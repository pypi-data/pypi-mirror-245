# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/nedbat/coveragepy/blob/master/NOTICE.txt

"""Coverage data for coverage.py.

This file had the 4.x JSON data support, which is now gone.  This file still
has storage-agnostic helpers, and is kept to avoid changing too many imports.
CoverageData is now defined in sqldata.py, and imported here to keep the
imports working.

"""

from __future__ import annotations

import glob
import hashlib
import os.path

from typing import Callable, Dict, Iterable, List, Optional

from coverage.exceptions import CoverageException, NoDataError
from coverage.files import PathAliases
from coverage.misc import Hasher, file_be_gone, human_sorted, plural
from coverage.sqldata import CoverageData


def line_counts(data: CoverageData, fullpath: bool = False) -> Dict[str, int]:
    """Return a dict summarizing the line coverage data.

    Keys are based on the file names, and values are the number of executed
    lines.  If `fullpath` is true, then the keys are the full pathnames of
    the files, otherwise they are the basenames of the files.

    Returns a dict mapping file names to counts of lines.

    """
    summ = {}
    filename_fn: Callable[[str], str]
    if fullpath:
        # pylint: disable=unnecessary-lambda-assignment
        filename_fn = lambda f: f
    else:
        filename_fn = os.path.basename
    for filename in data.measured_files():
        lines = data.lines(filename)
        assert lines is not None
        summ[filename_fn(filename)] = len(lines)
    return summ


def add_data_to_hash(data: CoverageData, filename: str, hasher: Hasher) -> None:
    """Contribute `filename`'s data to the `hasher`.

    `hasher` is a `coverage.misc.Hasher` instance to be updated with
    the file's data.  It should only get the results data, not the run
    data.

    """
    if data.has_arcs():
        hasher.update(sorted(data.arcs(filename) or []))
    else:
        hasher.update(sorted_lines(data, filename))
    hasher.update(data.file_tracer(filename))


def combinable_files(data_file: str, data_paths: Optional[Iterable[str]] = None) -> List[str]:
    """Make a list of data files to be combined.

    `data_file` is a path to a data file.  `data_paths` is a list of files or
    directories of files.

    Returns a list of absolute file paths.
    """
    data_dir, local = os.path.split(os.path.abspath(data_file))

    data_paths = data_paths or [data_dir]
    files_to_combine = []
    for p in data_paths:
        if os.path.isfile(p):
            files_to_combine.append(os.path.abspath(p))
        elif os.path.isdir(p):
            pattern = glob.escape(os.path.join(os.path.abspath(p), local)) +".*"
            files_to_combine.extend(glob.glob(pattern))
        else:
            raise NoDataError(f"Couldn't combine from non-existent path '{p}'")
    return files_to_combine


def combine_parallel_data(
    data: CoverageData,
    aliases: Optional[PathAliases] = None,
    data_paths: Optional[Iterable[str]] = None,
    strict: bool = False,
    keep: bool = False,
    message: Optional[Callable[[str], None]] = None,
) -> None:
    """Combine a number of data files together.

    `data` is a CoverageData.

    Treat `data.filename` as a file prefix, and combine the data from all
    of the data files starting with that prefix plus a dot.

    If `aliases` is provided, it's a `PathAliases` object that is used to
    re-map paths to match the local machine's.

    If `data_paths` is provided, it is a list of directories or files to
    combine.  Directories are searched for files that start with
    `data.filename` plus dot as a prefix, and those files are combined.

    If `data_paths` is not provided, then the directory portion of
    `data.filename` is used as the directory to search for data files.

    Unless `keep` is True every data file found and combined is then deleted
    from disk. If a file cannot be read, a warning will be issued, and the
    file will not be deleted.

    If `strict` is true, and no files are found to combine, an error is
    raised.

    `message` is a function to use for printing messages to the user.

    """
    files_to_combine = combinable_files(data.base_filename(), data_paths)

    if strict and not files_to_combine:
        raise NoDataError("No data to combine")

    file_hashes = set()
    combined_any = False

    for f in files_to_combine:
        if f == data.data_filename():
            # Sometimes we are combining into a file which is one of the
            # parallel files.  Skip that file.
            if data._debug.should("dataio"):
                data._debug.write(f"Skipping combining ourself: {f!r}")
            continue

        try:
            rel_file_name = os.path.relpath(f)
        except ValueError:
            # ValueError can be raised under Windows when os.getcwd() returns a
            # folder from a different drive than the drive of f, in which case
            # we print the original value of f instead of its relative path
            rel_file_name = f

        with open(f, "rb") as fobj:
            hasher = hashlib.new("sha3_256")
            hasher.update(fobj.read())
            sha = hasher.digest()
            combine_this_one = sha not in file_hashes

        delete_this_one = not keep
        if combine_this_one:
            if data._debug.should("dataio"):
                data._debug.write(f"Combining data file {f!r}")
            file_hashes.add(sha)
            try:
                new_data = CoverageData(f, debug=data._debug)
                new_data.read()
            except CoverageException as exc:
                if data._warn:
                    # The CoverageException has the file name in it, so just
                    # use the message as the warning.
                    data._warn(str(exc))
                if message:
                    message(f"Couldn't combine data file {rel_file_name}: {exc}")
                delete_this_one = False
            else:
                data.update(new_data, aliases=aliases)
                combined_any = True
                if message:
                    message(f"Combined data file {rel_file_name}")
        else:
            if message:
                message(f"Skipping duplicate data {rel_file_name}")

        if delete_this_one:
            if data._debug.should("dataio"):
                data._debug.write(f"Deleting data file {f!r}")
            file_be_gone(f)

    if strict and not combined_any:
        raise NoDataError("No usable data files")


def debug_data_file(filename: str) -> None:
    """Implementation of 'coverage debug data'."""
    data = CoverageData(filename)
    filename = data.data_filename()
    print(f"path: {filename}")
    if not os.path.exists(filename):
        print("No data collected: file doesn't exist")
        return
    data.read()
    print(f"has_arcs: {data.has_arcs()!r}")
    summary = line_counts(data, fullpath=True)
    filenames = human_sorted(summary.keys())
    nfiles = len(filenames)
    print(f"{nfiles} file{plural(nfiles)}:")
    for f in filenames:
        line = f"{f}: {summary[f]} line{plural(summary[f])}"
        plugin = data.file_tracer(f)
        if plugin:
            line += f" [{plugin}]"
        print(line)


def sorted_lines(data: CoverageData, filename: str) -> List[int]:
    """Get the sorted lines for a file, for tests."""
    lines = data.lines(filename)
    return sorted(lines or [])

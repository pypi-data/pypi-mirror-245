# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/nedbat/coveragepy/blob/master/NOTICE.txt

"""Miscellaneous stuff for coverage.py."""

from __future__ import annotations

import contextlib
import datetime
import errno
import hashlib
import importlib
import importlib.util
import inspect
import locale
import os
import os.path
import re
import sys
import types

from types import ModuleType
from typing import (
    Any, Callable, Dict, IO, Iterable, Iterator, List, Mapping, NoReturn, Optional,
    Sequence, Tuple, TypeVar, Union,
)

from coverage import env
from coverage.exceptions import CoverageException
from coverage.types import TArc

# In 6.0, the exceptions moved from misc.py to exceptions.py.  But a number of
# other packages were importing the exceptions from misc, so import them here.
# pylint: disable=unused-wildcard-import
from coverage.exceptions import *   # pylint: disable=wildcard-import

ISOLATED_MODULES: Dict[ModuleType, ModuleType] = {}


def isolate_module(mod: ModuleType) -> ModuleType:
    """Copy a module so that we are isolated from aggressive mocking.

    If a test suite mocks os.path.exists (for example), and then we need to use
    it during the test, everything will get tangled up if we use their mock.
    Making a copy of the module when we import it will isolate coverage.py from
    those complications.
    """
    if mod not in ISOLATED_MODULES:
        new_mod = types.ModuleType(mod.__name__)
        ISOLATED_MODULES[mod] = new_mod
        for name in dir(mod):
            value = getattr(mod, name)
            if isinstance(value, types.ModuleType):
                value = isolate_module(value)
            setattr(new_mod, name, value)
    return ISOLATED_MODULES[mod]

os = isolate_module(os)


class SysModuleSaver:
    """Saves the contents of sys.modules, and removes new modules later."""
    def __init__(self) -> None:
        self.old_modules = set(sys.modules)

    def restore(self) -> None:
        """Remove any modules imported since this object started."""
        new_modules = set(sys.modules) - self.old_modules
        for m in new_modules:
            del sys.modules[m]


@contextlib.contextmanager
def sys_modules_saved() -> Iterator[None]:
    """A context manager to remove any modules imported during a block."""
    saver = SysModuleSaver()
    try:
        yield
    finally:
        saver.restore()


def import_third_party(modname: str) -> Tuple[ModuleType, bool]:
    """Import a third-party module we need, but might not be installed.

    This also cleans out the module after the import, so that coverage won't
    appear to have imported it.  This lets the third party use coverage for
    their own tests.

    Arguments:
        modname (str): the name of the module to import.

    Returns:
        The imported module, and a boolean indicating if the module could be imported.

    If the boolean is False, the module returned is not the one you want: don't use it.

    """
    with sys_modules_saved():
        try:
            return importlib.import_module(modname), True
        except ImportError:
            return sys, False


def nice_pair(pair: TArc) -> str:
    """Make a nice string representation of a pair of numbers.

    If the numbers are equal, just return the number, otherwise return the pair
    with a dash between them, indicating the range.

    """
    start, end = pair
    if start == end:
        return "%d" % start
    else:
        return "%d-%d" % (start, end)


TSelf = TypeVar("TSelf")
TRetVal = TypeVar("TRetVal")

def expensive(fn: Callable[[TSelf], TRetVal]) -> Callable[[TSelf], TRetVal]:
    """A decorator to indicate that a method shouldn't be called more than once.

    Normally, this does nothing.  During testing, this raises an exception if
    called more than once.

    """
    if env.TESTING:
        attr = "_once_" + fn.__name__

        def _wrapper(self: TSelf) -> TRetVal:
            if hasattr(self, attr):
                raise AssertionError(f"Shouldn't have called {fn.__name__} more than once")
            setattr(self, attr, True)
            return fn(self)
        return _wrapper
    else:
        return fn                   # pragma: not testing


def bool_or_none(b: Any) -> Optional[bool]:
    """Return bool(b), but preserve None."""
    if b is None:
        return None
    else:
        return bool(b)


def join_regex(regexes: Iterable[str]) -> str:
    """Combine a series of regex strings into one that matches any of them."""
    regexes = list(regexes)
    if len(regexes) == 1:
        return regexes[0]
    else:
        return "|".join(f"(?:{r})" for r in regexes)


def file_be_gone(path: str) -> None:
    """Remove a file, and don't get annoyed if it doesn't exist."""
    try:
        os.remove(path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


def ensure_dir(directory: str) -> None:
    """Make sure the directory exists.

    If `directory` is None or empty, do nothing.
    """
    if directory:
        os.makedirs(directory, exist_ok=True)


def ensure_dir_for_file(path: str) -> None:
    """Make sure the directory for the path exists."""
    ensure_dir(os.path.dirname(path))


def output_encoding(outfile: Optional[IO[str]] = None) -> str:
    """Determine the encoding to use for output written to `outfile` or stdout."""
    if outfile is None:
        outfile = sys.stdout
    encoding = (
        getattr(outfile, "encoding", None) or
        getattr(sys.__stdout__, "encoding", None) or
        locale.getpreferredencoding()
    )
    return encoding


class Hasher:
    """Hashes Python data for fingerprinting."""
    def __init__(self) -> None:
        self.hash = hashlib.new("sha3_256")

    def update(self, v: Any) -> None:
        """Add `v` to the hash, recursively if needed."""
        self.hash.update(str(type(v)).encode("utf-8"))
        if isinstance(v, str):
            self.hash.update(v.encode("utf-8"))
        elif isinstance(v, bytes):
            self.hash.update(v)
        elif v is None:
            pass
        elif isinstance(v, (int, float)):
            self.hash.update(str(v).encode("utf-8"))
        elif isinstance(v, (tuple, list)):
            for e in v:
                self.update(e)
        elif isinstance(v, dict):
            keys = v.keys()
            for k in sorted(keys):
                self.update(k)
                self.update(v[k])
        else:
            for k in dir(v):
                if k.startswith("__"):
                    continue
                a = getattr(v, k)
                if inspect.isroutine(a):
                    continue
                self.update(k)
                self.update(a)
        self.hash.update(b".")

    def hexdigest(self) -> str:
        """Retrieve the hex digest of the hash."""
        return self.hash.hexdigest()[:32]


def _needs_to_implement(that: Any, func_name: str) -> NoReturn:
    """Helper to raise NotImplementedError in interface stubs."""
    if hasattr(that, "_coverage_plugin_name"):
        thing = "Plugin"
        name = that._coverage_plugin_name
    else:
        thing = "Class"
        klass = that.__class__
        name = f"{klass.__module__}.{klass.__name__}"

    raise NotImplementedError(
        f"{thing} {name!r} needs to implement {func_name}()"
    )


class DefaultValue:
    """A sentinel object to use for unusual default-value needs.

    Construct with a string that will be used as the repr, for display in help
    and Sphinx output.

    """
    def __init__(self, display_as: str) -> None:
        self.display_as = display_as

    def __repr__(self) -> str:
        return self.display_as


def substitute_variables(text: str, variables: Mapping[str, str]) -> str:
    """Substitute ``${VAR}`` variables in `text` with their values.

    Variables in the text can take a number of shell-inspired forms::

        $VAR
        ${VAR}
        ${VAR?}             strict: an error if VAR isn't defined.
        ${VAR-missing}      defaulted: "missing" if VAR isn't defined.
        $$                  just a dollar sign.

    `variables` is a dictionary of variable values.

    Returns the resulting text with values substituted.

    """
    dollar_pattern = r"""(?x)   # Use extended regex syntax
        \$                      # A dollar sign,
        (?:                     # then
            (?P<dollar>\$) |        # a dollar sign, or
            (?P<word1>\w+) |        # a plain word, or
            {                       # a {-wrapped
                (?P<word2>\w+)          # word,
                (?:
                    (?P<strict>\?) |        # with a strict marker
                    -(?P<defval>[^}]*)      # or a default value
                )?                      # maybe.
            }
        )
        """

    dollar_groups = ("dollar", "word1", "word2")

    def dollar_replace(match: re.Match[str]) -> str:
        """Called for each $replacement."""
        # Only one of the dollar_groups will have matched, just get its text.
        word = next(g for g in match.group(*dollar_groups) if g)    # pragma: always breaks
        if word == "$":
            return "$"
        elif word in variables:
            return variables[word]
        elif match["strict"]:
            msg = f"Variable {word} is undefined: {text!r}"
            raise CoverageException(msg)
        else:
            return match["defval"]

    text = re.sub(dollar_pattern, dollar_replace, text)
    return text


def format_local_datetime(dt: datetime.datetime) -> str:
    """Return a string with local timezone representing the date.
    """
    return dt.astimezone().strftime("%Y-%m-%d %H:%M %z")


def import_local_file(modname: str, modfile: Optional[str] = None) -> ModuleType:
    """Import a local file as a module.

    Opens a file in the current directory named `modname`.py, imports it
    as `modname`, and returns the module object.  `modfile` is the file to
    import if it isn't in the current directory.

    """
    if modfile is None:
        modfile = modname + ".py"
    spec = importlib.util.spec_from_file_location(modname, modfile)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)

    return mod


def _human_key(s: str) -> List[Union[str, int]]:
    """Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    def tryint(s: str) -> Union[str, int]:
        """If `s` is a number, return an int, else `s` unchanged."""
        try:
            return int(s)
        except ValueError:
            return s

    return [tryint(c) for c in re.split(r"(\d+)", s)]

def human_sorted(strings: Iterable[str]) -> List[str]:
    """Sort the given iterable of strings the way that humans expect.

    Numeric components in the strings are sorted as numbers.

    Returns the sorted list.

    """
    return sorted(strings, key=_human_key)

SortableItem = TypeVar("SortableItem", bound=Sequence[Any])

def human_sorted_items(
    items: Iterable[SortableItem],
    reverse: bool = False,
) -> List[SortableItem]:
    """Sort (string, ...) items the way humans expect.

    The elements of `items` can be any tuple/list. They'll be sorted by the
    first element (a string), with ties broken by the remaining elements.

    Returns the sorted list of items.
    """
    return sorted(items, key=lambda item: (_human_key(item[0]), *item[1:]), reverse=reverse)


def plural(n: int, thing: str = "", things: str = "") -> str:
    """Pluralize a word.

    If n is 1, return thing.  Otherwise return things, or thing+s.
    """
    if n == 1:
        return thing
    else:
        return things or (thing + "s")


def stdout_link(text: str, url: str) -> str:
    """Format text+url as a clickable link for stdout.

    If attached to a terminal, use escape sequences. Otherwise, just return
    the text.
    """
    if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
        return f"\033]8;;{url}\a{text}\033]8;;\a"
    else:
        return text

# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/nedbat/coveragepy/blob/master/NOTICE.txt

"""Support for plugins."""

from __future__ import annotations

import os
import os.path
import sys

from types import FrameType
from typing import Any, Dict, Iterable, Iterator, List, Optional, Set, Tuple, Union

from coverage.exceptions import PluginError
from coverage.misc import isolate_module
from coverage.plugin import CoveragePlugin, FileTracer, FileReporter
from coverage.types import (
    TArc, TConfigurable, TDebugCtl, TLineNo, TPluginConfig, TSourceTokenLines,
)

os = isolate_module(os)


class Plugins:
    """The currently loaded collection of coverage.py plugins."""

    def __init__(self) -> None:
        self.order: List[CoveragePlugin] = []
        self.names: Dict[str, CoveragePlugin] = {}
        self.file_tracers: List[CoveragePlugin] = []
        self.configurers: List[CoveragePlugin] = []
        self.context_switchers: List[CoveragePlugin] = []

        self.current_module: Optional[str] = None
        self.debug: Optional[TDebugCtl]

    @classmethod
    def load_plugins(
        cls,
        modules: Iterable[str],
        config: TPluginConfig,
        debug: Optional[TDebugCtl] = None,
    ) -> Plugins:
        """Load plugins from `modules`.

        Returns a Plugins object with the loaded and configured plugins.

        """
        plugins = cls()
        plugins.debug = debug

        for module in modules:
            plugins.current_module = module
            __import__(module)
            mod = sys.modules[module]

            coverage_init = getattr(mod, "coverage_init", None)
            if not coverage_init:
                raise PluginError(
                    f"Plugin module {module!r} didn't define a coverage_init function"
                )

            options = config.get_plugin_options(module)
            coverage_init(plugins, options)

        plugins.current_module = None
        return plugins

    def add_file_tracer(self, plugin: CoveragePlugin) -> None:
        """Add a file tracer plugin.

        `plugin` is an instance of a third-party plugin class.  It must
        implement the :meth:`CoveragePlugin.file_tracer` method.

        """
        self._add_plugin(plugin, self.file_tracers)

    def add_configurer(self, plugin: CoveragePlugin) -> None:
        """Add a configuring plugin.

        `plugin` is an instance of a third-party plugin class. It must
        implement the :meth:`CoveragePlugin.configure` method.

        """
        self._add_plugin(plugin, self.configurers)

    def add_dynamic_context(self, plugin: CoveragePlugin) -> None:
        """Add a dynamic context plugin.

        `plugin` is an instance of a third-party plugin class.  It must
        implement the :meth:`CoveragePlugin.dynamic_context` method.

        """
        self._add_plugin(plugin, self.context_switchers)

    def add_noop(self, plugin: CoveragePlugin) -> None:
        """Add a plugin that does nothing.

        This is only useful for testing the plugin support.

        """
        self._add_plugin(plugin, None)

    def _add_plugin(
        self,
        plugin: CoveragePlugin,
        specialized: Optional[List[CoveragePlugin]],
    ) -> None:
        """Add a plugin object.

        `plugin` is a :class:`CoveragePlugin` instance to add.  `specialized`
        is a list to append the plugin to.

        """
        plugin_name = f"{self.current_module}.{plugin.__class__.__name__}"
        if self.debug and self.debug.should("plugin"):
            self.debug.write(f"Loaded plugin {self.current_module!r}: {plugin!r}")
            labelled = LabelledDebug(f"plugin {self.current_module!r}", self.debug)
            plugin = DebugPluginWrapper(plugin, labelled)

        plugin._coverage_plugin_name = plugin_name
        plugin._coverage_enabled = True
        self.order.append(plugin)
        self.names[plugin_name] = plugin
        if specialized is not None:
            specialized.append(plugin)

    def __bool__(self) -> bool:
        return bool(self.order)

    def __iter__(self) -> Iterator[CoveragePlugin]:
        return iter(self.order)

    def get(self, plugin_name: str) -> CoveragePlugin:
        """Return a plugin by name."""
        return self.names[plugin_name]


class LabelledDebug:
    """A Debug writer, but with labels for prepending to the messages."""

    def __init__(self, label: str, debug: TDebugCtl, prev_labels: Iterable[str] = ()):
        self.labels = list(prev_labels) + [label]
        self.debug = debug

    def add_label(self, label: str) -> LabelledDebug:
        """Add a label to the writer, and return a new `LabelledDebug`."""
        return LabelledDebug(label, self.debug, self.labels)

    def message_prefix(self) -> str:
        """The prefix to use on messages, combining the labels."""
        prefixes = self.labels + [""]
        return ":\n".join("  "*i+label for i, label in enumerate(prefixes))

    def write(self, message: str) -> None:
        """Write `message`, but with the labels prepended."""
        self.debug.write(f"{self.message_prefix()}{message}")


class DebugPluginWrapper(CoveragePlugin):
    """Wrap a plugin, and use debug to report on what it's doing."""

    def __init__(self, plugin: CoveragePlugin, debug: LabelledDebug) -> None:
        super().__init__()
        self.plugin = plugin
        self.debug = debug

    def file_tracer(self, filename: str) -> Optional[FileTracer]:
        tracer = self.plugin.file_tracer(filename)
        self.debug.write(f"file_tracer({filename!r}) --> {tracer!r}")
        if tracer:
            debug = self.debug.add_label(f"file {filename!r}")
            tracer = DebugFileTracerWrapper(tracer, debug)
        return tracer

    def file_reporter(self, filename: str) -> Union[FileReporter, str]:
        reporter = self.plugin.file_reporter(filename)
        assert isinstance(reporter, FileReporter)
        self.debug.write(f"file_reporter({filename!r}) --> {reporter!r}")
        if reporter:
            debug = self.debug.add_label(f"file {filename!r}")
            reporter = DebugFileReporterWrapper(filename, reporter, debug)
        return reporter

    def dynamic_context(self, frame: FrameType) -> Optional[str]:
        context = self.plugin.dynamic_context(frame)
        self.debug.write(f"dynamic_context({frame!r}) --> {context!r}")
        return context

    def find_executable_files(self, src_dir: str) -> Iterable[str]:
        executable_files = self.plugin.find_executable_files(src_dir)
        self.debug.write(f"find_executable_files({src_dir!r}) --> {executable_files!r}")
        return executable_files

    def configure(self, config: TConfigurable) -> None:
        self.debug.write(f"configure({config!r})")
        self.plugin.configure(config)

    def sys_info(self) -> Iterable[Tuple[str, Any]]:
        return self.plugin.sys_info()


class DebugFileTracerWrapper(FileTracer):
    """A debugging `FileTracer`."""

    def __init__(self, tracer: FileTracer, debug: LabelledDebug) -> None:
        self.tracer = tracer
        self.debug = debug

    def _show_frame(self, frame: FrameType) -> str:
        """A short string identifying a frame, for debug messages."""
        return "%s@%d" % (
            os.path.basename(frame.f_code.co_filename),
            frame.f_lineno,
        )

    def source_filename(self) -> str:
        sfilename = self.tracer.source_filename()
        self.debug.write(f"source_filename() --> {sfilename!r}")
        return sfilename

    def has_dynamic_source_filename(self) -> bool:
        has = self.tracer.has_dynamic_source_filename()
        self.debug.write(f"has_dynamic_source_filename() --> {has!r}")
        return has

    def dynamic_source_filename(self, filename: str, frame: FrameType) -> Optional[str]:
        dyn = self.tracer.dynamic_source_filename(filename, frame)
        self.debug.write("dynamic_source_filename({!r}, {}) --> {!r}".format(
            filename, self._show_frame(frame), dyn,
        ))
        return dyn

    def line_number_range(self, frame: FrameType) -> Tuple[TLineNo, TLineNo]:
        pair = self.tracer.line_number_range(frame)
        self.debug.write(f"line_number_range({self._show_frame(frame)}) --> {pair!r}")
        return pair


class DebugFileReporterWrapper(FileReporter):
    """A debugging `FileReporter`."""

    def __init__(self, filename: str, reporter: FileReporter, debug: LabelledDebug) -> None:
        super().__init__(filename)
        self.reporter = reporter
        self.debug = debug

    def relative_filename(self) -> str:
        ret = self.reporter.relative_filename()
        self.debug.write(f"relative_filename() --> {ret!r}")
        return ret

    def lines(self) -> Set[TLineNo]:
        ret = self.reporter.lines()
        self.debug.write(f"lines() --> {ret!r}")
        return ret

    def excluded_lines(self) -> Set[TLineNo]:
        ret = self.reporter.excluded_lines()
        self.debug.write(f"excluded_lines() --> {ret!r}")
        return ret

    def translate_lines(self, lines: Iterable[TLineNo]) -> Set[TLineNo]:
        ret = self.reporter.translate_lines(lines)
        self.debug.write(f"translate_lines({lines!r}) --> {ret!r}")
        return ret

    def translate_arcs(self, arcs: Iterable[TArc]) -> Set[TArc]:
        ret = self.reporter.translate_arcs(arcs)
        self.debug.write(f"translate_arcs({arcs!r}) --> {ret!r}")
        return ret

    def no_branch_lines(self) -> Set[TLineNo]:
        ret = self.reporter.no_branch_lines()
        self.debug.write(f"no_branch_lines() --> {ret!r}")
        return ret

    def exit_counts(self) -> Dict[TLineNo, int]:
        ret = self.reporter.exit_counts()
        self.debug.write(f"exit_counts() --> {ret!r}")
        return ret

    def arcs(self) -> Set[TArc]:
        ret = self.reporter.arcs()
        self.debug.write(f"arcs() --> {ret!r}")
        return ret

    def source(self) -> str:
        ret = self.reporter.source()
        self.debug.write("source() --> %d chars" % (len(ret),))
        return ret

    def source_token_lines(self) -> TSourceTokenLines:
        ret = list(self.reporter.source_token_lines())
        self.debug.write("source_token_lines() --> %d tokens" % (len(ret),))
        return ret

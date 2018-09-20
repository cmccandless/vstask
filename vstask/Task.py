"""See
https://code.visualstudio.com/docs/editor/tasks-appendix#_schema-for-tasksjson
"""
import os
from aenum import Enum
from .type_validation import (
    validate,
    validate_dict,
    validate_enum,
    validate_list,
)


class TaskType(Enum):
    _init_ = 'value __doc__'
    SHELL = 0,  """Execute inside a shell"""
    PROCESS = 1,  """Execute as a new process"""


class ShellConfiguration(object):
    def __init__(self, executable, args=None):
        """
        Positional arguments:
        executable(str) -- The shell to use.
        args(list(str)) -- The arguments to be passed to the shell executable
                           to run in command mode (e.g ['-c'] for bash or
                           ['/S', '/C'] for cmd.exe).
        """
        self.executable = validate('executable', executable, str)
        if args is None:
            self.args = []
        else:
            self.args = validate_list('args', args, str)


class CommandOptions(object):
    """Options to be passed to the external program or shell"""
    def __init__(self, shell, cwd=None, env=None):
        """
        Positional arguments:
        shell(ShellConfiguration) -- Configuration of the shell when task type
                                     is `shell`
        Keyword arguments:
        cwd(str)            -- The current working directory of the executed
                            program or shell. If omitted the current
                            workspace's root is used.
        env(dict(str, str)) -- The environment of the executed program or
                               shell. If omitted the parent process'
                               environment is used.
        """
        self.shell = validate('shell', shell, str)
        if cwd is None:
            self.cwd = None
        else:
            self.cwd = validate('cwd', cwd, str)
        if env is None:
            self.env = None
        else:
            self.env = validate_dict('env', env, (str,), (str,))


class RevealOptions(Enum):
    _init_ = 'value __doc__'
    ALWAYS = 0,   """Always show output"""
    SILENT = 1,   """Only show output on error"""
    NEVER = 2,    """Never show output"""


class PanelOptions(Enum):
    _init_ = 'value __doc__'
    SHARED = 0,  """Share between tasks"""
    DEDICATED = 1,  """Use for current task only"""
    NEW = 2,  """Create new panel on task execution"""


class PresentationOptions(object):
    def __init__(self, reveal=RevealOptions.ALWAYS, echo=True, focus=True,
                 panel=PanelOptions.SHARED):
        """
        Keyword arguments:
        reveal(RevealOptions) -- Controls whether the task output is revealed
                                 in the user interface.
        echo(bool)            -- Controls whether the command associated with
                                 the task is echoed in the user interface.
        focus(bool)           -- Controls whether the panel showing the task
                                 output is taking focus.
        panel(PanelOptions)   -- Controls task panel behavior.
        """
        self.reveal = validate_enum('reveal', reveal, RevealOptions)
        self.echo = validate('echo', echo, bool)
        self.focus = validate('focus', focus, bool)
        self.panel = validate_enum('panel', panel, PanelOptions)


class GroupKind(Enum):
    BUILD = 0,
    TEST = 1,


class GroupDescription(object):
    def __init__(self, kind, is_default=False):
        """
        Positional arguments:
        kind(GroupKind)  -- Task group.
        is_default(bool) -- Indicates whether this is the default task for the
                            specified group.
        """
        self.kind = validate_enum('kind', kind, GroupKind)
        self.is_default = validate('is_default', is_default, bool)


class Severity(Enum):
    ERROR = 0,
    WARNING = 1,
    INFO = 2,


class FileLocation(object):
    def __init__(self, absolute=True, relative_path=None):
        """
        Keyword arguments:
        absolute(bool)     -- Treat filepaths as absolute (False for relative).
        relative_path(str) -- Treat filepaths as relative to this path.
                              Current working directory is used if not given.
        """
        self.absolute = validate('absolute', absolute, bool)
        if relative_path is None:
            self.relative_path = os.getcwd()
        else:
            self.relative_path = validate("relative_path", relative_path, str)


class BackgroundMatcher(object):
    """A description to track the start and end of a background task."""
    def __init__(self, active_on_start=True, begins_pattern=None,
                 ends_pattern=None):
        """
        Keyword arguments:
        active_on_start(bool) -- If set to true the watcher is in active mode
                                 when the task starts. This is equals of
                                 issuing a line that matches the beginPattern.
        begins_pattern(str)   -- If matched in the output the start of a
                                 background task is signaled.
        ends_pattern(str)     -- If matched in the output the end of a
                                 background task is signaled.
        """
        self.active_on_start = validate(
            "active_on_start", active_on_start, bool
        )
        if begins_pattern is None:
            self.begins_pattern = None
        else:
            self.begins_pattern = validate(
                "begins_pattern", begins_pattern, str
            )
        if ends_pattern is None:
            self.ends_pattern = None
        else:
            self.ends_pattern = validate(
                "ends_pattern", ends_pattern, str
            )


class ProblemPatternKind(Enum):
    _init_ = 'value __doc__'
    FILE = 0,  """Match whole file"""
    LOCATION = 1,  """Match location in file"""


class ProblemPatternLocation(object):
    def __init__(self, line, column=1, end_line=None, end_column=None):
        self.line = validate("line", line, int)
        self.column = validate("column", column, int)
        self.end_line = validate("end_line", end_line, int)
        self.end_column = validate("end_column", end_column, int)


class ProblemPattern(object):
    def __init__(self, regexp, file, kind=ProblemPatternKind.LOCATION,
                 location=None, line=None, column=None, end_line=None,
                 end_column=None, severity=None, code=0, loop=False):
        """
        Positional arguments:
        regexp(str) -- The regular expression to find a problem in the console
                       output of an executed task.
        file(int)   -- The match group index of the filename.
        Keyword arguments:
        kind(ProblemPatternKind)        -- Whether the pattern matches a
                                           problem for the whole file or for a
                                           location inside a file.
        location(ProblemPatternLocation) -- The match group index of the
                                           problem's location. If omitted the
                                           line and column properties are used.
        line(int)                       -- The match group index of the
                                           problem's line in the source file.
                                           Can only be omitted if location is
                                           specified.
        column(int)                     -- The match group index of the
                                           problem's column in the source file.
        end_line(int)                   -- The match group index of the
                                           problem's end line in the source
                                           file. Defaults to undefined. No end
                                           line is captured.
        end_column(int)                 -- The match group index of the
                                           problem's end column in the source
                                           file. Defaults to undefined. No end
                                           column is captured.
        severity(Severity)              -- The match group index of the
                                           problem's severity. Defaults to
                                           undefined. In this case the problem
                                           matcher's severity is used.
        code(int)                       -- The match group index of
                                           the message.
        loop(bool)                      -- Specifies if the last pattern in a
                                           multi line problem matcher should
                                           loop as long as it does match a
                                           line consequently. Only valid on
                                           the last problem pattern in a multi
                                           line problem matcher.
        """
        self.regexp = validate("regexp", regexp, str)
        self.file = validate("file", file, int)
        self.kind = validate_enum("kind", kind, ProblemPatternKind)
        if location is None:
            self.location = None
        else:
            self.location = validate(
                "location", location, ProblemPatternLocation
            )
        if line is None:
            if location is None:
                raise ValueError(
                    'line may only be omitted if location is provided'
                )
            self.line = None
        else:
            self.line = validate("line", line, int)
        if column is None:
            self.column = None
        else:
            self.column = validate("column", column, int)
        if end_line is None:
            self.end_line = None
        else:
            self.end_line = validate("end_line", end_line, int)
        if end_column is None:
            self.end_column = None
        else:
            self.end_column = validate("end_column", end_column, int)
        if severity is None:
            self.severity = None
        else:
            self.severity = validate_enum("severity", severity, Severity)
        self.code = validate("code", code, int)
        self.loop = validate("loop", loop, bool)


class ProblemMatcher(object):
    """ A description of a problem matcher that detects problems in build output.
    """
    def __init__(self, base=None, owner='external', severity=Severity.ERROR,
                 file_location=None, pattern=None, background=None):
        """
        Keyword arguments:
        base(str)                     -- The name of a base problem matcher to
                                         use. If specified the base problem
                                         matcher will be used as a template
                                         and properties specified here will
                                         replace properties of the base
                                         problem matcher.
        owner(str)                    -- The owner of the produced VS Code
                                         problem. This is typically the
                                         identifier of a VS Code language
                                         service if the problems are to be
                                         merged with the one produced by the
                                         language service or 'external'.
        severity(Severity)            -- The severity of the VS Code problem
                                         produced by this problem matcher.The
                                         value is used if a pattern doesn't
                                         specify a severity match group.
        file_location(FileLocation)   -- Defines how filename reported in a
                                         problem pattern should be read.
        pattern(list(ProblemPattern)) -- The name of a predefined problem
                                         pattern, the inline definition of a
                                         problem pattern or an array of
                                         problem patterns to match problems
                                         spread over multiple lines.
        background(BackgroundMatcher) -- Additional information used to detect
                                         when a background task (like a
                                         watching task in Gulp) is active.
        """
        if base is None:
            self.base = None
        else:
            self.base = validate("base", base, str)
        self.owner = validate("owner", owner, str)
        self.severity = validate_enum("severity", severity, Severity)
        if file_location is None:
            self.file_location = None
        else:
            self.file_location = validate(
                "file_location", file_location, FileLocation
            )
        if pattern is None:
            self.pattern = None
        else:
            self.pattern = validate_list("pattern", pattern, ProblemPattern)
        if background is None:
            self.background = None
        else:
            self.background = validate(
                "background", background, BackgroundMatcher
            )


class TaskDescription(object):
    """The description of a task."""
    def __init__(self, label, type, command, is_background=True, args=None,
                 group=None, presentation=None, problem_matcher=None):
        """
        Positional arguments:
        label(str)     -- The task's name.
        type(TaskType) -- The type of a custom task. Tasks of type "shell" are
                          executed inside a shell (e.g. bash, cmd,
                          powershell, ...)
        command(str)   -- The command to be executed. Can be an external
                          program or a shell command.
        Keyword arguments:
        is_background(bool)               -- Specifies whether a global
                                             command is a background task.
        args(list(str))                   -- The arguments passed to the
                                             command.
        group(GroupDescription)           -- Defines the group to which this
                                             task belongs. Also supports to
                                             mark a task as the default task
                                             in a group.
        presentation(PresentationOptions) -- The presentation options.
        problem_matcher(ProblemMatcher)   -- The problem matcher to be used if
                                             a global command is executed.
        """
        self.label = validate("label", label, str)
        self.type = validate_enum("type", type, TaskType)
        self.command = validate("command", command, str)
        self.is_background = validate("is_background", is_background, bool)
        if args is None:
            self.args = None
        else:
            self.args = validate_list("args", args, str)
        if group is None:
            self.group = None
        else:
            self.group = validate("group", group, GroupDescription)
        if presentation is None:
            self.presentation = None
        else:
            self.presentation = validate(
                "presentation", presentation, PresentationOptions
            )
        if problem_matcher is None:
            self.problem_matcher = None
        else:
            self.problem_matcher = validate(
                "problem_matcher", problem_matcher, ProblemMatcher
            )


class BaseTaskConfiguration(object):
    def __init__(self, type, command, is_background=True, options=None,
                 args=None, presentation=None, problem_matcher=None,
                 tasks=None):
        """
        Positional arguments:
        type(TaskType) -- The type of a custom task. Tasks of type "shell" are
                         executed inside a shell (e.g. bash, cmd,
                         powershell, ...)
        command(str)   -- The command to be executed. Can be an external
                          program or a shell command.
        Keyword arguments:
        is_background(bool)               -- Specifies whether a global
                                             command is a background task.
        options(CommandOptions)           -- The command options used when the
                                             command is executed.
        args(list(str))                   -- The arguments passed to the
                                             command.
        presentation(PresentationOptions) -- The presentation options.
        problem_matcher(ProblemMatcher)   -- The problem matcher to be used if
                                             a global command is executed.
        tasks(list(TaskDescription))      -- The configuration of the
                                             available tasks.
        """
        self.type = validate_enum("type", type, TaskType)
        self.command = validate("command", command, str)
        self.is_background = validate("is_background", is_background, bool)
        if options is None:
            self.options = None
        else:
            self.options = validate("options", options, CommandOptions)
        if args is None:
            self.args = None
        else:
            self.args = validate_list("args", args, str)
        if presentation is None:
            self.presentation = None
        else:
            self.presentation = validate(
                "presentation", presentation, PresentationOptions
            )
        if problem_matcher is None:
            self.problem_matcher = None
        else:
            self.problem_matcher = validate(
                "problem_matcher", problem_matcher, ProblemMatcher
            )
        if tasks is None:
            self.tasks = None
        else:
            self.tasks = validate_list("tasks", tasks, TaskDescription)


class TaskConfiguration(BaseTaskConfiguration):
    def __init__(self, type, command, is_background=True, options=None,
                 args=None, presentation=None, problem_matcher=None,
                 tasks=None, version='2.0.0', windows=None, osx=None,
                 linux=None):
        """
        Positional arguments:
        type(TaskType) -- The type of a custom task. Tasks of type "shell" are
                         executed inside a shell (e.g. bash, cmd,
                         powershell, ...)
        command(str)   -- The command to be executed. Can be an external
                          program or a shell command.
        Keyword arguments:
        is_background(bool)               -- Specifies whether a global
                                             command is a background task.
        options(CommandOptions)           -- The command options used when the
                                             command is executed.
        args(list(str))                   -- The arguments passed to the
                                             command.
        presentation(PresentationOptions) -- The presentation options.
        problem_matcher(ProblemMatcher)   -- The problem matcher to be used if
                                             a global command is executed.
        tasks(list(TaskDescription))      -- The configuration of the
                                             available tasks.
        version(str)                      -- The configuration's version number
        windows(BaseTaskConfiguration)    -- Windows specific task
                                             configuration
        osx(BaseTaskConfiguration)        -- macOS specific task configuration
        linux(BaseTaskConfiguration)      -- Linux specific task configuration
        """
        BaseTaskConfiguration.__init__(
            self, type, command, is_background, options, args, presentation,
            problem_matcher, tasks
        )
        self.version = validate("version", version, str)
        if windows is None:
            self.windows = None
        else:
            self.windows = validate("windows", windows, BaseTaskConfiguration)
        if osx is None:
            self.osx = None
        else:
            self.osx = validate("osx", osx, BaseTaskConfiguration)
        if linux is None:
            self.linux = None
        else:
            self.linux = validate("linux", linux, BaseTaskConfiguration)

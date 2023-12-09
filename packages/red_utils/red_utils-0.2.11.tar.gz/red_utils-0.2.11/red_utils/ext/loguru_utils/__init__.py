## Import default constants
from __future__ import annotations

from . import constants, enums, operations, sinks, validators
from .constants import (
    LogLevel,
    default_color_fmt,
    default_fmt,
    log_levels,
    uvicorn_log_conf,
    valid_compression_strs,
)
from .enums import EnumDefaultSinks, EnumLogLevels
from .operations import add_sink, init_logger
from .sinks import (
    DefaultSinks,
    LoguruSinkAppFile,
    LoguruSinkDefault,
    LoguruSinkErrFile,
    LoguruSinkFileDefault,
    LoguruSinkStdErr,
    LoguruSinkStdOut,
    LoguruSinkTraceFile,
)

# from .sinks import (
#     default_app_log_file_sink,
#     default_error_log_file_sink,
#     default_sinks,
#     default_stderr_color_sink,
#     default_stderr_sink,
#     default_stdout_color_sink,
#     default_stdout_sink,
#     default_trace_log_file_sink,
# )
from .validators import validate_compression_str, validate_level, validate_logger

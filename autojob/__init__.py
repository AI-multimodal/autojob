"""The autojob code contains a complete set of default files based on the
developers' primary use cases. These defaults are enumerated in this core
module. The user can override any and all defaults by providing their own
config files in `~/.autojob`. This directory will be created if it does not
exist, and any config files in the defaults that do not exist in the directory
will be created if they do not exist (TODO)."""

from pathlib import Path
import sys

from loguru import logger

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


# Set the logging style


def generic_filter(names):
    if names == "all":
        return None

    def f(record):
        return record["level"].name in names

    return f


logger.remove(0)  # Remove the default logger

OUT_FMT = "<lvl>{message}</>"


STDOUT_LOGGER_ID = logger.add(
    sys.stdout,
    colorize=True,
    filter=generic_filter(["INFO", "SUCCESS"]),
    format=OUT_FMT,
)

ERR_FMT = "<lvl>{level}:</> <lvl>{message}</>"

STDERR_LOGGER_ID = logger.add(
    sys.stderr,
    colorize=True,
    filter=generic_filter(["WARNING", "ERROR", "CRITICAL"]),
    format=ERR_FMT,
)

ROOT = Path.home() / Path(".autojob")
if not ROOT.exists():
    ROOT.mkdir(exist_ok=False, parents=True)


FMT2 = (
    "<k>{time:YYYY-MM-DD HH:mm:ss.SSS}</> "
    "<k>{name}</>:<k>{function}</>:<k>{line}</> "
    "[<lvl>{level}</>] <lvl>{message}</>"
)

LOGFILE_LOGGER_ID = logger.add(
    ROOT / Path("LOGS"),
    filter=generic_filter("all"),
    format=FMT2,
    rotation="2.0 GB",
)

import argparse
from argparse import HelpFormatter, ArgumentDefaultsHelpFormatter
from operator import attrgetter

# from os import getpid
# from os import kill as kill_pid
# from signal import SIGTERM
# from pathlib import Path
import sys

# from time import sleep, time

from autojob import logger, STDOUT_LOGGER_ID, OUT_FMT, generic_filter
from autojob.report import generate_report


# https://stackoverflow.com/questions/
# 12268602/sort-argparse-help-alphabetically
class SortingHelpFormatter(ArgumentDefaultsHelpFormatter, HelpFormatter):
    def add_arguments(self, actions):
        actions = sorted(actions, key=attrgetter("option_strings"))
        super(SortingHelpFormatter, self).add_arguments(actions)


def global_parser(sys_argv):
    ap = argparse.ArgumentParser(formatter_class=SortingHelpFormatter)

    ap.add_argument(
        "--debug",
        dest="debug",
        default=False,
        action="store_true",
        help="If specified, enables the DEBUG stream to stdout.",
    )

    # --- Global options ---

    subparsers = ap.add_subparsers(help="Global options", dest="runtype")

    report_subparser = subparsers.add_parser(
        "report",
        formatter_class=SortingHelpFormatter,
        description="Generates a report based on a recursive search of a "
        "directory. Different types of scientific calculations are supported, "
        "and are tabulated in the documentation. At the simplest level, a "
        "job is marked as successfully completed, failed or unknown.",
    )

    report_subparser.add_argument(
        "root", help="Path to the directory to analyze."
    )

    report_subparser.add_argument(
        "-f",
        "--filename",
        dest="filename",
        default="submit.sbatch",
        help="Filename to search for.",
    )

    return ap.parse_args(sys_argv)


def enable_debug(logger_id=STDOUT_LOGGER_ID):
    logger.remove(logger_id)
    logger.add(
        sys.stdout,
        colorize=True,
        filter=generic_filter(["DEBUG", "INFO", "SUCCESS"]),
        format=OUT_FMT,
    )


def entrypoint():
    """Point of entry from the command line interface.

    Raises
    ------
    RuntimeError
        If unknown runtime types are provided.
    """

    args = global_parser(sys.argv[1:])
    if args.debug:
        enable_debug()

    if args.runtype == "report":
        generate_report(args.root, args.filename)

    elif args.runtype == "modify":
        pass

    else:
        raise RuntimeError(f"Unknown runtime type {args.runtype}")

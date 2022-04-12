"""The tether module is designed to perform non-trivial actions to construct
submission scripts. For example, consider a situation where you have many jobs
to submit, but each job is cheap and does not require significant
parallelization. Perhaps each job is even faster than a minute (the minimum
cronjob time)."""

from copy import copy
from math import floor, log10
from pathlib import Path
import sys

from tqdm import tqdm

from autojob import logger
from autojob.file_utils import exhaustive_directory_search


def chunks(lst, n):
    """See https://stackoverflow.com/questions/312443/
    how-do-you-split-a-list-into-evenly-sized-chunks.

    Parameters
    ----------
    lst : TYPE
        Description
    n : TYPE
        Description

    Yields
    ------
    TYPE
        Description
    """

    for ii in range(0, len(lst), n):
        yield lst[ii : ii + n]


def get_file_lines(slurm_header_lines, chunk, executable_line):

    file_lines = copy(slurm_header_lines) + [""]
    for dd in chunk:
        file_lines.append(f"cd {dd.absolute()}")
        file_lines.append(executable_line)
    file_lines.append("\nwait\nexit")
    return file_lines


def tether_constructor(
    root,
    filename,
    staging_directory,
    calculations_per_staged_job,
    slurm_header_lines,
    executable_line,
):
    """Summary

    Parameters
    ----------
    root : TYPE
        Description
    filename : TYPE
        Description
    staging_directory : TYPE
        Description
    calculations_per_staged_job : TYPE
        Description
    slurm_header_lines : TYPE
        Description
    executable_line : TYPE
        Description
    """

    logger.info(f"Tethering jobs for {root}, looking for filename {filename}")
    logger.info(f"Staging to {staging_directory}")
    logger.info(f"Calculations per staged job: {calculations_per_staged_job}")
    logger.info(f"Executable line: {executable_line}")
    logger.debug(f"Slurm header is {slurm_header_lines}")
    directories = exhaustive_directory_search(root, filename)
    chunked_directories = list(chunks(directories, calculations_per_staged_job))

    if "&" not in executable_line:
        logger.critical(
            f"& is not found in the executable line {executable_line}. "
            "These are required for the tether_constructor to allow jobs to "
            "run in parallel. Tether has not written anything. Exiting."
        )
        sys.exit(1)

    logger.info("Constructing the chunked directory lines")
    submit_script_lines = []
    for chunk in tqdm(chunked_directories):

        # For each chunk, we write a single SLURM script which changes
        # directories into the one where the executable should be
        lines = get_file_lines(slurm_header_lines, chunk, executable_line)
        submit_script_lines.append(lines)

    # Now save those jobs to the appropriate directory structure
    L = len(submit_script_lines)
    logger.info(f"Saving {L} submit scripts to staging directory")
    oom = floor(log10(L)) + 1
    target_root = Path(staging_directory)
    for ii, submit_script in enumerate(tqdm(submit_script_lines)):
        dd = target_root / Path(str(ii).zfill(oom))
        dd.mkdir(exist_ok=False, parents=True)
        with open(dd / Path("submit.sbatch"), "w") as f:
            for line in submit_script:
                f.write(f"{line}\n")

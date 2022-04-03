"""Module for generating reports on the results of input files.

.. important::

    While this should work generally, autojob is currently tested on the
    following types of code: FEFF 9.9.1, VASP 6.2.1, and the default CONFIG
    assumes these code versions.
"""

from pathlib import Path

from autojob import CONFIG
from autojob.file_utils import (
    exhaustive_directory_search,
    run_command,
    check_if_substring_match,
)


def check_computation_type(root, input_files=CONFIG["report.in"]):
    """Determines which type of computation has been completed in the directory
    of interest.

    Parameters
    ----------
    root : os.PathLike
        The directory containing the

    Returns
    -------
    str
        The type of calculation that the directory contains. The available
        options are found in DEFAULT_INPUT_FILES.
    """

    contained = {xx.parts[-1] for xx in list(Path(root).iterdir())}
    overlap = {
        key: set(value).issubset(contained)
        for key, value in input_files.items()
    }

    # Check to see if for some reason there are multiple computations' input
    # files in one directory. This obvious is a problem.
    assert sum(list(overlap.values())) == 1

    # Otherwise, we simply find which one is true
    return [key for key, value in overlap.items() if value][0]


def check_job_status(root, checks):
    """Checks the status of a job by looking in the directory of interest for
    the appropriate completion status. This function does not check that the
    provided root directory actually corresponds to the type of calculation
    provided will error ungracefully if it does not contain the appropriate
    files. Output files have their last 100 lines checked.

    Parameters
    ----------
    root : os.PathLike
        The directory containing input and output files.
    checks : list of list of str
        A doubly nested list. The outer lists correspond to filename-substring
        pairs. If the substring is None, then this will simply check whether or
        not the file exists and is not empty.

    Returns
    -------
    bool
        True if the job has completed successfully, False otherwise.
    """

    for filename, substring in checks:
        path = Path(root) / Path(filename)

        # Check for existence and that the file size is > 0
        if substring is None:
            if not path.exists():
                return False
            if path.stat().st_size == 0:
                return False
            return True

        command = f"tail -n 100 {str(path)}"
        res = run_command(command)
        lines = res["stdout"].split("\n")
        cond = check_if_substring_match(lines, str(substring))

        if not cond:
            return False

    return True


def generate_report(root, filename, output_files=CONFIG["report.out"]):
    """Generates a report of which jobs have finished, which are still ongoing
    and which have failed. Currently, returns True if the job completed with
    seemingly no issues, and False otherwise.

    Notes
    -----
    What is checked given some calculation type is detailed below:
    * VASP: If the job completed, the OUTCAR file will contain timing
    information.
    * FEFF: If the job completed, there will be a non-empty xmu.dat file.

    Parameters
    ----------
    root : os.PathLike
        Root location for the exhaustive directory search.
    filename : str
        Looks exhaustively in root for directories containing a file matching
        this name.
    identifiers : dict, optional
        A dictionary containing strings as keys, which identify the computation
        type, and sets as values, which identify input files that all must be
        contained in the directory to identify the directory as corresponding
        to a certain computation type. Default is DEFAULT_INPUT_FILES.

    Returns
    -------
    dict
        A dictionary with keys as the paths to the directories checked and
        boolean values, indicating the success status of the calculation.
    """

    # Get the directories matching the filename of the directory search
    directories = exhaustive_directory_search(root, filename)

    # For each directory in the tree, determine the type of calculation that
    # was run.
    calculation_types = {dd: check_computation_type(dd) for dd in directories}

    # Get the statuses
    status = {
        dd: check_job_status(dd, checks=output_files[ctype])
        for dd, ctype in calculation_types.items()
    }

    return status

"""Module for generating reports on the results of input files."""

from pathlib import Path

from autojob.file_utils import exhaustive_directory_search, run_command


DEFAULT_INPUT_FILES = {
    "FEFF": set(["inp.feff"]),
    "VASP": set(["INCAR", "POSCAR", "KPOINTS", "POTCAR"]),
}


def check_computation_type(root):
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

    contained = set([xx.stem for xx in list(Path(root).iterdir())])
    overlap = {key: contained == value for key, value in DEFAULT_INPUT_FILES}

    # Check to see if for some reason there are multiple computations' input
    # files in one directory. This obvious is a problem.
    assert sum(list(overlap.values())) == 1

    # Otherwise, we simply find which one is true
    return [key for key, value in overlap.items() if value][0]


def check_VASP_job_status(root):
    """Checks the status of a VASP job by looking in the directory of interest
    for the appropriate completion status. Does not check against any job
    controller status. This is done separately. This also does not check that
    the provided root directory is actually a VASP results-containing one, and
    will error ungracefully if it does not contain the OUTCAR file from a VASP
    calculation.

    .. important::

        While this should generally work, the code is currently tested on
        VASP 6.2.1

    Parameters
    ----------
    root : os.PathLike
        The directory containing VASP input and output files.

    Returns
    -------
    bool
        True if the job has completed (the timing information was found in the
        OUTCAR file). False otherwise. Note that False does not imply job
        failure, it could mean that the job is still in progress.
    """

    # Get the last 50 lines of the file, this should be sufficient for
    # containing the timing information.
    path = Path(root) / Path("OUTCAR")
    command = f"tail -n 50 {path}"
    res = run_command(command)

    # Check for the string of interest
    look_for = " General timing and accounting informations for this job:"
    return look_for in res["stdout"].split("\n")


def check_FEFF_job_status(root):
    """Checks the status of a FEFF job by looking in the directory of interest
    for the appropriate completion status. Does not check against any job
    controller status. This is done separately. This also does not check that
    the provided root directory is actually a FEFF results-containing one, and
    will error ungracefully if it does not contain the feff.out file from a
    FEFF calculation. Note this code also checks for the xmu.dat file, which is
    always output upon successful FEFF calculation.

    .. important::

        While this should generally work, the code is currently tested on
        FEFF 9.9.1

    Parameters
    ----------
    root : os.PathLike
        The directory containing FEFF input and output files.

    Returns
    -------
    bool
        True if the job has completed (the completion information was found in
        the feff.out file). False otherwise. Note that False does not imply job
        failure, it could mean that the job is still in progress.
    """

    # Check for the xmu.dat, which will exist and be non-empty if the
    # calculation completed successfully
    xmu_path = Path(root) / Path("xmu.dat")
    if not xmu_path.exists():
        return False
    if xmu_path.stat().st_size == 0:
        return False

    path = Path(root) / Path("feff.out")

    # Check the last few lines of the feff.out file
    command = f"tail -n 10 {path}"
    res = run_command(command)

    # Check for the string of interest. In FEFF, this will usually be the
    # second to last line, but to be sure we'll look at all 10. Note as well
    # that the look_for lines needs to be found via substring match since the
    # date is printed in the output line.
    look_for = "feff ends at"
    in_lines = [look_for in xx for xx in res["stdout"].split("\n")]
    assert sum(in_lines) < 2
    return True if sum(in_lines) == 1 else False


def check_job_status(root, calculation_type):
    """Summary

    Parameters
    ----------
    root : TYPE
        Description
    calculation_type : TYPE
        Description
    """

    if calculation_type == "FEFF":
        return check_FEFF_job_status(root)
    elif calculation_type == "VASP":
        return check_VASP_job_status(root)

    raise ValueError(f"Unknown calculation type {calculation_type}")


def generate_report(root, filename, identifiers=DEFAULT_INPUT_FILES):
    """Generates a report of which jobs have finished, which are still ongoing
    and which have failed. Currently, returns True if the job completed with
    seemingly no issues, and False otherwise.

    .. important::

        Currently tested on: VASP 6.2.1, FEFF 9.9.1.

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

    Notes
    -----
    What is checked given some calculation type is detailed below:
    - VASP: If the job completed, the OUTCAR file will contain timing
      information (see e.g. here: github.com/aiida-vasp/aiida-vasp/issues/287).
    - FEFF: If the job completed, there will be a non-empty xmu.dat file.

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
    status = {dd: calculation_types[dd] for dd in calculation_types.keys()}

    return status

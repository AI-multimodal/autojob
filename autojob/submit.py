from monty.json import MSONable
from pathlib import Path

from autojob import logger
from autojob.file_utils import save_json, read_json, run_command


ROOT = Path.home() / Path(".autojob") / Path("submit")
QUEUE_LOC = ROOT / Path("SubmitQueue.json")
PARAMS_LOC = ROOT / Path("params.json")

if PARAMS_LOC.exists():
    PARAMS = read_json(PARAMS_LOC)
else:
    logger.warning("~/.autojob/submit/params.json does not exist")
    PARAMS = None


def get_slurm_job_status(user=None):
    """Summary
    
    Parameters
    ----------
    user : TYPE, optional
        Description
    """

    if user is None:
        if PARAMS is not None:
            user = PARAMS["user"]
        else:
            out = run_command("whoami")
            user = out["stdout"]
            logger.warning(f"Using whoami for SLURM user: {user}")

    command = "squeue -u mcarbone | awk 'NR!=1'"
    out = run_command(command)
    if int(out["exitcode"]) != 0:
        raise RuntimeError(f"Uknown error running get_slurm_job_status {out}")
    slurm_out = [xx.split() for xx in out["stdout"].split("\n")]

    # Transpose trick
    slurm_out = list(map(list, zip(*slurm_out)))

    # Assert everything came from the same user
    assert len(set(slurm_out[3])) == 1

    # Compile everything to a dictionary
    return dict(
        job_ids=slurm_out[0],
        partitions=slurm_out[1],
        job_names=slurm_out[2],
        statuses=slurm_out[4],
        running_time=slurm_out[5],
        nodes=slurm_out[6],
        nodelist=slurm_out[7]
    )


class Job(MSONable):

    @property
    def directory(self):
        return self._directory

    @property
    def script_name(self):
        return self._script_name
    
    @property
    def priority(self):
        return self._priority
    
    def __init__(
        self,
        directory,
        script_name="submit.sbatch",
        priority=0,
    ):
        self._directory = str(directory)
        self._script_name = str(script_name)
        self._priority = priority


class SubmitQueue(MSONable):

    def save(self, path=QUEUE_LOC):
        """Saves the SubmitQueue object to disk as a json file."""

        save_json(self.as_dict(), path)

    @classmethod
    def load(cls, path=QUEUE_LOC):
        """Loads the class from serialized json file.
        
        Parameters
        ----------
        path : os.PathLike
        
        Returns
        -------
        SubmitQueue
        """

        if not path.exists():
            return cls()
        return cls.from_dict(read_json(path))

    @property
    def queue(self):
        """A list of :class:`.Job` objects.
        
        Returns
        -------
        list of Job
        """

        return self._queue
    
    def __init__(self, path=QUEUE_LOC, queue=[]):
        Path(path).parent.mkdir(exist_ok=True, parents=True)
        self._path = path
        self._queue = queue

    def _append_queue_(self, job):
        """Extends the current queue with new directories to run from.
        
        Parameters
        ----------
        submit_lines : list of os.PathLike
            A list of lines to submit.

            .. example::

                submit_lines = [
                    "sbatch /first/path"
                ]
        """

        if not isinstance(job, Job):
            logger.error(f"Provided job {job} must be of instance Job")
            return
        self._queue.append(job)

    def add_(self, directory, script_name="submit.sbatch", priority=0.0):
        """Adds a job to the queue.
        
        Parameters
        ----------
        directory : os.PathLike
            The location containing the ``script_name``.
        script_name : str, optional
            The name of the script.
        priority : float, optional
            The relative priority of the job.
        """

        logger.info(
            f"Appending job: dir={directory} | script_name={script_name} | "
            f"priority={priority}"
        )
        self._append_queue_(Job(directory, script_name, priority))

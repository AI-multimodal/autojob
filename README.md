# autojob

[![codecov](https://codecov.io/gh/AI-multimodal/autojob/branch/master/graph/badge.svg?token=HTZQRGHULG)](https://codecov.io/gh/AI-multimodal/autojob)

Simple utility for controlling linux jobs and handling error tracking in scientific code.

* Free software: 3-clause BSD license
* Documentation: (COMING SOON!) https://x94carbone.github.io/autojob.

The project philosophy should follow the following three key points, and of course, all code should be well-documented, well-tested and readable.

* **Lightweight**: as close to pure python as possible
* **User-friendly**: as easy to use as possible
* **Complete logging**: everything is logged


## Current goals

* Given a list of directories, find all subdirectories containing a certain script name, e.g. submit.sbatch, and execute those jobs.
* Keep track of the job controller (SLURM as a first case) and keep the queue topped off every N seconds.
* Self-terminate when all jobs have completed.
* Log the error/completion status of the jobs (this depends on the scientific code that is run, and is not as simple as just checking e.g. slurm.err.
* Generate a report for the user.


## Contributing

If you want to help develop this code, you should do the following:

* Create a fresh virtual environment, e.g. `conda create -n py3.9 python=3.9`.
* Install the development requirements, `pip install -r requirements-dev.txt`
* Setup the pre-commit hooks `pre-commit install`
* If you want to install the package to your default paths, you can do this in "developer mode" by running `pip install -e ".[dev]"`

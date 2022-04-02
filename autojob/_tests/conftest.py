from pathlib import Path
import pytest
from tempfile import TemporaryDirectory


class DummyDirectories(TemporaryDirectory):
    """A helper utility class for temporarily creating a large directory
    structure for tests to be conducted in. Will cleanup when done. The
    directories used are actually based on real input files using VASP, FEFF,
    etc."""

    def __enter__(self):
        """Constructs a dummy directory structure for testing methods that act
        on input files."""

        name = super().__enter__()

        d1 = [
            "mp-1179358",
            "mp-636827",
            "mvc-11423",
            "mp-25433",
            "mp-655656",
            "mvc-11600",
            "mp-390",
            "mp-685151",
        ]

        d2 = ["FEFF-XANES", "VASP"]

        input_files = {
            "FEFF-XANES": ["feff.inp"],
            "VASP": ["INCAR", "KPOINTS", "POSCAR", "POTCAR"],
        }

        for x1 in d1:
            for x2 in d2:
                path = Path(name) / Path(f"{x1}/{x2}")
                path.mkdir(parents=True, exist_ok=False)

                for inp in input_files[x2]:
                    (path / Path(inp)).touch()

                # Write the dummy submit scripts for everything except for
                # mp-390
                if x1 != "mp-390":
                    (path / Path("submit.sbatch")).touch()

        return name


@pytest.fixture
def dummydirectories():
    return DummyDirectories()


@pytest.fixture
def dummyVASPOutcarSuccess():
    return """
   34        1.558   3.465   0.000   0.000   5.023
   35        1.558   3.464   0.000   0.000   5.022
   36        1.558   3.465   0.000   0.000   5.023
   37        1.558   3.465   0.000   0.000   5.023
   38        1.558   3.463   0.000   0.000   5.021
   39        1.558   3.464   0.000   0.000   5.022
   40        1.557   3.435   0.000   0.000   4.993
   41        1.558   3.465   0.000   0.000   5.023
   42        1.558   3.463   0.000   0.000   5.021
   43        1.558   3.465   0.000   0.000   5.023
   44        1.558   3.463   0.000   0.000   5.021
   45        1.558   3.464   0.000   0.000   5.022
   46        1.558   3.465   0.000   0.000   5.023
   47        1.558   3.464   0.000   0.000   5.022
   48        1.558   3.465   0.000   0.000   5.023
--------------------------------------------------
tot         85.498 208.787  22.849   0.632 317.765



 magnetization (x)

# of ion       s       p       d       f       tot
--------------------------------------------------
    1        0.008   0.005   0.213   0.000   0.226
    2        0.000  -0.000   0.001  -0.000   0.000
    3       -0.000  -0.000  -0.000  -0.000  -0.000
    4        0.000  -0.000   0.000  -0.000  -0.000
    5       -0.000  -0.000  -0.000  -0.000  -0.000
    6        0.000  -0.000   0.000  -0.000  -0.000
    7        0.000  -0.001   0.005  -0.000   0.004
    8        0.000  -0.000   0.000  -0.000  -0.000
    9       -0.000  -0.000  -0.000  -0.000  -0.000
   10        0.000  -0.000   0.001  -0.000   0.000
   11        0.000  -0.001   0.005  -0.000   0.004
   12        0.000  -0.000   0.001  -0.000   0.000
   13        0.000   0.000   0.002  -0.000   0.002
   14        0.000  -0.000   0.000  -0.000  -0.000
   15       -0.000  -0.000  -0.000  -0.000  -0.000
   16        0.000  -0.000   0.001  -0.000   0.000
   17       -0.000  -0.026   0.000   0.000  -0.027
   18       -0.001  -0.031   0.000   0.000  -0.032
   19       -0.000  -0.026   0.000   0.000  -0.027
   20       -0.001  -0.031   0.000   0.000  -0.032
   21       -0.000  -0.002   0.000   0.000  -0.002
   22       -0.000  -0.000   0.000   0.000  -0.000
   23       -0.000  -0.002   0.000   0.000  -0.002
   24       -0.000  -0.000   0.000   0.000  -0.000
   25       -0.000  -0.002   0.000   0.000  -0.002
   26       -0.000  -0.001   0.000   0.000  -0.001
   27       -0.000  -0.002   0.000   0.000  -0.002
   28       -0.000  -0.000   0.000   0.000  -0.000
   29       -0.000  -0.003   0.000   0.000  -0.003
   30       -0.001  -0.031   0.000   0.000  -0.032
   31       -0.000  -0.001   0.000   0.000  -0.001
   32       -0.000  -0.003   0.000   0.000  -0.003
   33       -0.000  -0.002   0.000   0.000  -0.002
   34       -0.000  -0.000   0.000   0.000  -0.000
   35       -0.000  -0.002   0.000   0.000  -0.002
   36       -0.000  -0.001   0.000   0.000  -0.001
   37       -0.000  -0.001   0.000   0.000  -0.001
   38       -0.000  -0.003   0.000   0.000  -0.003
   39       -0.000  -0.003   0.000   0.000  -0.003
   40       -0.001  -0.031   0.000   0.000  -0.032
   41       -0.000  -0.001   0.000   0.000  -0.001
   42       -0.000  -0.003   0.000   0.000  -0.003
   43       -0.000  -0.001   0.000   0.000  -0.001
   44       -0.000  -0.003   0.000   0.000  -0.003
   45       -0.000  -0.002   0.000   0.000  -0.002
   46       -0.000  -0.001   0.000   0.000  -0.001
   47       -0.000  -0.002   0.000   0.000  -0.002
   48       -0.000  -0.001   0.000   0.000  -0.001
--------------------------------------------------
tot          0.003  -0.213   0.227  -0.000   0.016


 total amount of memory used by VASP MPI-rank0  7033136. kBytes
=======================================================================

   base      :      30000. kBytes
   nonlr-proj:     142446. kBytes
   fftplans  :      71598. kBytes
   grid      :     223232. kBytes
   one-center:       7746. kBytes
   wavefun   :    6558114. kBytes



 General timing and accounting informations for this job:
 ========================================================

                  Total CPU time used (sec):     4167.709
                            User time (sec):     3672.045
                          System time (sec):      495.664
                         Elapsed time (sec):     4178.002

                   Maximum memory used (kb):     9871916.
                   Average memory used (kb):          N/A

                          Minor page faults:      1353021
                          Major page faults:           11
                 Voluntary context switches:       212100
"""

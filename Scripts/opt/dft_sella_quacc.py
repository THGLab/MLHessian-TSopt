
"""
Original Author: Samuel Blau
Modifier: Anup Kumar

Module for adding calculations to a FireWorks LaunchPad.

Includes functions to add transition state and IRC (Intrinsic Reaction Coordinate)
calculations to a LaunchPad for QChem using the FireWorks workflow management tool.

"""

import toml
import glob
import jobflow as jf
from ase import Atoms
from ase.io import read
from fireworks import LaunchPad
from quacc.recipes.qchem.ts import ts_job
from quacc.recipes.qchem.ts import irc_job
from quacc.recipes.qchem.core import freq_job
from jobflow.managers.fireworks import flow_to_workflow


def add_to_launchpad(
        index: str,
        atoms: Atoms,
        tag: str,
        lpad: LaunchPad,
        run_job_locally: bool = False,
        RUN: bool = False,
) -> None:
    """
    Add QChem calculations to a LaunchPad.

    Parameters:
        index (str): Identifier for the calculation.
        atoms (Atoms): ASE Atoms object representing the molecular structure.
        tag (str): Tag to classify the calculation.
        lpad (LaunchPad): FireWorks LaunchPad object.
        run_job_locally (bool, optional): Whether to run the job locally. Defaults to False.
        RUN (bool, optional): Whether to add the workflow to the LaunchPad. Defaults to False.

    Returns:
        None
    """
    job1 = ts_job(
                  atoms,
                  0,
                  1,
                  method="wb97x",
                  basis="6-31G*",
                 )
    job1.name = f"ind{index}_{tag}_ts"

    job1f = freq_job(
                     job1.output,
                     0,
                     1,
                     method="wb97x",
                     basis="6-31G*",
                    )
    job1f.name = f"ind{index}_{tag}_freq"

    job2 = irc_job(
                   job1.output,
                   0,
                   1,
                   direction="forward",
                   method="wb97x",
                   basis="6-31G*",
                  )
    job2.name = f"ind{index}_{tag}_firc"

    job2f = freq_job(
                     job2.output,
                     0,
                     1,
                     method="wb97x",
                     basis="6-31G*",
                    )
    job2f.name = f"ind{index}_{tag}_firc_freq"

    job3 = irc_job(
                   job1.output,
                   0,
                   1,
                   direction="reverse",
                   method="wb97x",
                   basis="6-31G*",
                  )
    job3.name = f"ind{index}_{tag}_rirc"

    job3f = freq_job(
                     job3.output,
                     0,
                     1,
                     method="wb97x",
                     basis="6-31G*"
                    )
    job3f.name = f"ind{index}_{tag}_rirc_freq"

    job_list = [job1, job1f, job2, job2f, job3, job3f]

    for job in job_list:
        job.update_metadata(
            {
                "class": f"{tag}"
            }
        )

    flow = jf.Flow(job_list)

    if run_job_locally:
        responses = jf.run_locally(flow)
        result = responses[job2.uuid][1].output
        print(result)
    else:
        wf = flow_to_workflow(flow)

        if RUN:
            lpad.add_wf(wf)


def main() -> None:
    """
    Main function to add QChem calculations to the LaunchPad.

    Returns:
        None
    """
    config = toml.load('inputs/config44.toml')

    index_files = [index_file for index_file in glob.glob(config['indices']['xyz_files_dir'] + '/*')]
    tag = config['general']['tag']
    run = config['general']['run']
    LAUNCHPAD_FILE = config['general']['launchpad_file']
    lpad = LaunchPad.from_file(LAUNCHPAD_FILE)

    for index_file in index_files:
        atoms = read(index_file)
        index = index_file.split('/')[-1].split('.')[0]
        add_to_launchpad(
            index,
            atoms,
            tag,
            lpad,
            RUN=run,
        )


if __name__ == '__main__':
    main()

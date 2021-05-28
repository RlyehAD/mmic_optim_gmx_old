# Import models
from mmic_optim.models.output import OptimOutput
from mmelemental.models import Molecule, Trajectory
from ..models import GmxComputeOutput

# Import components
from mmic.components.blueprints import GenericComponent

from typing import List, Tuple, Optional
import os
import shutil

__all__ = ["GmxPostComponent"]


class GmxPostComponent(GenericComponent):
    @classmethod
    def input(cls):
        return GmxComputeOutput

    @classmethod
    def output(cls):
        return OptimOutput

    def execute(
        self,
        inputs: GmxComputeOutput,
        extra_outfiles: Optional[List[str]] = None,
        extra_commands: Optional[List[str]] = None,
        scratch_name: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> Tuple[bool, OptimOutput]:

        """
        This method translate the output of em
        to mmic schema. But right now it can only
        be applied to single molecule conditions
        """

        traj_file = inputs.trajectory
        if inputs.proc_input.trajectory is None:
            traj_name = list(inputs.proc_input.molecule)[0]
            traj = {traj_name: Trajectory.from_file(traj_file)}
        else:
            traj_name = list(inputs.proc_input.trajectory)[0]
            traj_files = {traj_name: traj_file}
            traj = {
                key: Trajectory.from_file(trajs_files[key])
                for key in inputs.proc_input.trajectory
            }

        mol_file = inputs.molecule
        mol_name = list(inputs.proc_input.molecule)[0]
        mol_files = {mol_name: mol_file}
        mol = {
            key: Molecule.from_file(mol_files[key])
            for key in inputs.proc_input.molecule
        }
        self.cleanup([inputs.scratch_dir])

        return True, OptimOutput(
            proc_input=inputs.proc_input, molecule=mol, trajectory=traj
        )

    @staticmethod
    def cleanup(remove: List[str]):
        for item in remove:
            if os.path.isdir(item):
                shutil.rmtree(item)
            elif os.path.isfile(item):
                os.remove(item)

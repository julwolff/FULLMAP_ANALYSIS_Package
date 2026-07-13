import MDAnalysis as mda
import numpy as np

from analyses.dynamics.msd import compute_msd
from analyses.structure.rdf import compute_rdf
from analyses.structure.coordination import compute_coordination
from analyses.structure.distortion import compute_distortion
from analyses.structure.xrd import compute_xrd_series

from analyses.thermodynamics.energy import extract_energy_from_log

u = mda.Universe(
    "in.data",
    "cool_dump.lammpstrj",
    atom_style="id type x y z",
    format="LAMMPSDUMP"
)

n_frames = len(u.trajectory)
time = np.arange(n_frames) * 0.020

compute_msd(u, time)

compute_rdf(u)

compute_coordination(u)

compute_distortion(u)

extract_energy_from_log()

compute_xrd_series(u)

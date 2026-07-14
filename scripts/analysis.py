#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main analysis driver.

All parameters are stored in:

    config/analysis_config.py

All analysis switches are stored in:

    config/analysis_selection.py
"""

# ==========================================================
# IMPORTS
# ==========================================================

import MDAnalysis as mda
import numpy as np

# ==========================================================
# CONFIGURATION
# ==========================================================

from config.analysis_config import *
from config.analysis_selection import *

# ==========================================================
# ANALYSES
# ==========================================================

from analyses.dynamics import (
    run_msd_analysis,
    compute_jumps,
    compute_residence_times
)

from analyses.structure import (
    compute_rdf_segments,
    compute_coordination,
    compute_distortion,
    compute_xrd_series
)

from analyses.thermodynamics import (
    extract_energy_from_log
)

from analyses.sites import (
    assign_sites_trajectory,
    compute_site_occupancy,
    find_vacancies,
    find_antisites
)

# ==========================================================
# LOAD TRAJECTORY
# ==========================================================

print("")
print("==================================================")
print(" LOADING TRAJECTORY")
print("==================================================")

u = mda.Universe(
    TOPOLOGY_FILE,
    TRAJ_FILE_NAME,
    atom_style="id type x y z",
    format="LAMMPSDUMP"
)

n_frames = len(u.trajectory)

time = np.arange(n_frames) * TIMESTEP

print(f"Trajectory : {TRAJ_FILE_NAME}")
print(f"Topology   : {TOPOLOGY_FILE}")
print(f"Frames     : {n_frames}")

# ==========================================================
# ENERGY
# ==========================================================

if RUN_ENERGY:

    print("")
    print("==================================================")
    print(" ENERGY")
    print("==================================================")

    extract_energy_from_log(
        logfile=LOG_FILE,
        step_min=STEP_MIN,
        step_max=STEP_MAX
    )

# ==========================================================
# MSD + DIFFUSION
# ==========================================================

if RUN_MSD:

    print("")
    print("==================================================")
    print(" MSD + DIFFUSION")
    print("==================================================")

    run_msd_analysis(
        u,
        time,
        {
            "Li": TYPE_LI,
            "Mn": TYPE_MN,
            "O": TYPE_O
        }
    )

# ==========================================================
# RDF
# ==========================================================

if RUN_RDF:

    print("")
    print("==================================================")
    print(" RDF")
    print("==================================================")

    compute_rdf_segments(
        u,
        TYPE_MN,
        TYPE_O,
        n_segments=RDF_SEGMENTS
    )

# ==========================================================
# COORDINATION
# ==========================================================

if RUN_COORDINATION:

    print("")
    print("==================================================")
    print(" COORDINATION")
    print("==================================================")

    compute_coordination(
        u,
        center_selection=TYPE_MN,
        neighbor_selection=TYPE_O,
        cutoff=CUTOFF_MNO
    )

# ==========================================================
# DISTORTION
# ==========================================================

if RUN_DISTORTION:

    print("")
    print("==================================================")
    print(" DISTORTION")
    print("==================================================")

    compute_distortion(
        u,
        center_selection=TYPE_MN,
        oxygen_selection=TYPE_O,
        cutoff=CUTOFF_MNO
    )

# ==========================================================
# XRD
# ==========================================================

if RUN_XRD:

    print("")
    print("==================================================")
    print(" XRD")
    print("==================================================")

    compute_xrd_series(
        u,
        wavelength=WAVELENGTH,
        twotheta_min=TWOTHETA_MIN,
        twotheta_max=TWOTHETA_MAX,
        dump_every=DUMP_EVERY,
        xrd_every=XRD_EVERY,
        xrd_window=XRD_WINDOW
    )

# ==========================================================
# SITE ASSIGNMENT
# ==========================================================

if RUN_SITE_ASSIGNMENT:

    print("")
    print("==================================================")
    print(" SITE ASSIGNMENT")
    print("==================================================")

    assign_sites_trajectory(
        u,
        sites_file=SITE_FILE
    )

# ==========================================================
# OCCUPANCY
# ==========================================================

if RUN_SITE_OCCUPANCY:

    print("")
    print("==================================================")
    print(" SITE OCCUPANCY")
    print("==================================================")

    compute_site_occupancy(
        assignment_file="site_assignment.dat"
    )

# ==========================================================
# JUMPS
# ==========================================================

if RUN_JUMPS:

    print("")
    print("==================================================")
    print(" JUMP ANALYSIS")
    print("==================================================")

    compute_jumps(
        assignment_file="site_assignment.dat"
    )

# ==========================================================
# RESIDENCE TIMES
# ==========================================================

if RUN_RESIDENCE:

    print("")
    print("==================================================")
    print(" RESIDENCE TIMES")
    print("==================================================")

    compute_residence_times(
        assignment_file="site_assignment.dat",
        timestep_ps=TIMESTEP
    )

# ==========================================================
# DEFECT ANALYSIS
# ==========================================================

if RUN_DEFECTS:

    print("")
    print("==================================================")
    print(" DEFECT ANALYSIS")
    print("==================================================")

    find_vacancies()
    find_antisites()

# ==========================================================
# FUTURE ANALYSES
# ==========================================================

if RUN_VOLUME:

    print("")
    print("Volume analysis not yet implemented")

if RUN_COLLECTIVE_DIFFUSION:

    print("")
    print("Collective diffusion not yet implemented")

if RUN_DIFFUSION_NETWORK:

    print("")
    print("Diffusion network not yet implemented")

# ==========================================================
# DONE
# ==========================================================

print("")
print("==================================================")
print(" ANALYSIS COMPLETE")
print("==================================================")
print("")

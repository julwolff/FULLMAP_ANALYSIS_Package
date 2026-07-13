#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main analysis driver.

Individual analyses are implemented in:

    analyses/
        dynamics/
        structure/
        thermodynamics/
        sites/
"""

import MDAnalysis as mda
import numpy as np

# ==========================================================
# PARAMETERS
# ==========================================================

TOPOLOGY = "in.data"

TRAJECTORY = "XX_TRAJECTORY_XX"

TYPE_LI = "type 1"
TYPE_MN = "type 2"
TYPE_O  = "type 3"

TIMESTEP = 0.020   # ps

# ----------------------------------------------------------
# Energy
# ----------------------------------------------------------

LOGFILE = "log.lammps"

STEP_MIN = 10000
STEP_MAX = 2010000

# ----------------------------------------------------------
# RDF
# ----------------------------------------------------------

RDF_SEGMENTS = 10

# ----------------------------------------------------------
# Coordination / Distortion
# ----------------------------------------------------------

CUTOFF_MNO = 2.5

# ----------------------------------------------------------
# XRD
# ----------------------------------------------------------

WAVELENGTH = "CuKa"

TWOTHETA_MIN = 10
TWOTHETA_MAX = 90

DUMP_EVERY = 1000

XRD_EVERY = 200000
XRD_WINDOW = 20000

# ----------------------------------------------------------
# Site analysis
# ----------------------------------------------------------

RUN_SITE_ANALYSIS = False

SITE_FILE = "sites.dat"

# ==========================================================
# IMPORT ANALYSES
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
    compute_site_occupancy
)

# ==========================================================
# LOAD TRAJECTORY
# ==========================================================

print("")
print("========================================")
print(" LOADING TRAJECTORY")
print("========================================")

u = mda.Universe(
    TOPOLOGY,
    TRAJECTORY,
    atom_style="id type x y z",
    format="LAMMPSDUMP"
)

n_frames = len(u.trajectory)

time = np.arange(n_frames) * TIMESTEP

print(f"Frames : {n_frames}")

# ==========================================================
# ENERGY
# ==========================================================

print("")
print("========================================")
print(" ENERGY")
print("========================================")

extract_energy_from_log(
    logfile=LOGFILE,
    step_min=STEP_MIN,
    step_max=STEP_MAX
)

# ==========================================================
# MSD + DIFFUSION
# ==========================================================

print("")
print("========================================")
print(" MSD")
print("========================================")

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

print("")
print("========================================")
print(" RDF")
print("========================================")

compute_rdf_segments(
    u,
    TYPE_MN,
    TYPE_O,
    n_segments=RDF_SEGMENTS
)

# ==========================================================
# COORDINATION
# ==========================================================

print("")
print("========================================")
print(" COORDINATION")
print("========================================")

compute_coordination(
    u,
    center_selection=TYPE_MN,
    neighbor_selection=TYPE_O,
    cutoff=CUTOFF_MNO
)

# ==========================================================
# DISTORTION
# ==========================================================

print("")
print("========================================")
print(" DISTORTION")
print("========================================")

compute_distortion(
    u,
    center_selection=TYPE_MN,
    oxygen_selection=TYPE_O,
    cutoff=CUTOFF_MNO
)

# ==========================================================
# XRD
# ==========================================================

print("")
print("========================================")
print(" XRD")
print("========================================")

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
# SITE ANALYSIS
# ==========================================================

if RUN_SITE_ANALYSIS:

    print("")
    print("========================================")
    print(" SITE ASSIGNMENT")
    print("========================================")

    assign_sites_trajectory(
        u,
        sites_file=SITE_FILE
    )

    print("")
    print("========================================")
    print(" SITE OCCUPANCY")
    print("========================================")

    compute_site_occupancy()

    print("")
    print("========================================")
    print(" JUMPS")
    print("========================================")

    compute_jumps()

    print("")
    print("========================================")
    print(" RESIDENCE TIMES")
    print("========================================")

    compute_residence_times(
        timestep_ps=TIMESTEP
    )

# ==========================================================
# DONE
# ==========================================================

print("")
print("========================================")
print(" ANALYSIS COMPLETE")
print("========================================")

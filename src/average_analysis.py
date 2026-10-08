#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 17:14:48 2026

@author: jwjules
"""


import glob
import os

from config.averaging_selection import AVERAGING
from config.analysis_config import matrix_atom_type


from src.averaging.matrix import average_matrix
from src.averaging.diffusion import average_diffusion
from src.averaging.occupancy import average_site_occupancy
from src.averaging.residence import average_residence_time
from src.averaging.xrd import average_xrd
from src.averaging.count_sites_changes import count_site_type_changes
from src.averaging.matrix_jumps import site_transition_matrix
from src.averaging.LCA import accumulate_local_structures


# ==========================================================
# HELPERS
# ==========================================================

def get_files(name):

    return sorted(
        glob.glob(
            f"Structure_*/{name}.dat"
        )
    )


# ==========================================================
# MAIN
# ==========================================================

print("")
print("==================================================")
print(" AVERAGING ANALYSIS")
print("==================================================")

# ----------------------------------------------------------
# MATRIX FILES
# ----------------------------------------------------------

matrix_files = [

    "msd_Li",
    "msd_Mn",
    "msd_O",

    "rdf_evolution",

    "coord_Mn",

    "distortion",

    "energy"
]

for name in matrix_files:

    if not AVERAGING.get(name, False):
        continue

    files = get_files(name)

    if len(files) == 0:

        print(
            f"[SKIP] {name}"
        )

        continue

    print(
        f"[AVERAGE] {name}"
    )

    average_matrix(
        files,
        f"avg_{name}.dat"
    )

# ----------------------------------------------------------
# DIFFUSION
# ----------------------------------------------------------

if AVERAGING.get(
        "diffusion",
        False):

    files = get_files(
        "diffusion"
    )

    if len(files):

        print(
            "[AVERAGE] diffusion"
        )

        average_diffusion(
            files,
            "avg_diffusion.dat"
        )

# ----------------------------------------------------------
# OCCUPANCY
# ----------------------------------------------------------

if AVERAGING.get(
        "site_occupancy",
        False):
    
    print("debug")

    files = get_files(
        "site_assignment"
    )

    if len(files):

        print(
            "[AVERAGE] site_occupancy"
        )

        average_site_occupancy(
            files,
            "avg_site_occupancy.dat"
        )

# ----------------------------------------------------------
# RESIDENCE TIMES
# ----------------------------------------------------------

if AVERAGING.get(
        "residence_time",
        False):

    files = get_files(
        "residence_time"
    )

    if len(files):

        print(
            "[AVERAGE] residence_time"
        )

        average_residence_time(
            files,
            "avg_residence_time.dat"
        )

# ----------------------------------------------------------
# SITES CHANGE
# ----------------------------------------------------------

if AVERAGING.get(
        "count_sites_change",
        False):

    files = get_files(
        "site_assignment"
    )

    if len(files):

        print(
            "[COMPUTE] sites jumps"
        )

        count_site_type_changes(
            files,
            "avg_sites_jumps.dat"
        )


# ----------------------------------------------------------
# SITES MATRIX
# ----------------------------------------------------------

if AVERAGING.get(
        "matrix_jumps",
        False):

    files = get_files(
        "site_assignment"
    )

    if len(files):

        print(
            "[COMPUTE] sites matrix"
        )

        site_transition_matrix(
            files,
            "avg_sites_matrix.dat",
            matrix_atom_type
        )

# ----------------------------------------------------------
# XRD
# ----------------------------------------------------------

if AVERAGING.get(
        "xrd",
        False):

    print(
        "[AVERAGE] XRD"
    )

    reference = glob.glob(
        "Structure_1/xrd_*.dat"
    )

    for file in reference:

        basename = os.path.basename(
            file
        )

        files = sorted(
            glob.glob(
                f"Structure_*/{basename}"
            )
        )

        if len(files) == 0:
            continue

        average_xrd(
            files,
            f"avg_{basename}"
        )
        
# ----------------------------------------------------------
# LCA
# ----------------------------------------------------------

if AVERAGING.get(
        "LCA",
        False):

    print(
        "[AVERAGE] LCA"
    )

    files = get_files(
        "LCA"
    )

    if len(files):

        print(
            "[COMPUTE] sites jumps"
        )

        accumulate_local_structures(
            files,
            "avg_LCA.dat"
        )

# ==========================================================
# DONE
# ==========================================================

print("")
print("==================================================")
print(" AVERAGING COMPLETE")
print("==================================================")
print("")
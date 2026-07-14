#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Run all requested averaging operations.

Controlled through:

    config/averaging_selection.py
"""

import os
import subprocess
import glob

from config.averaging_selection import AVERAGING

# ==========================================================
# PATHS
# ==========================================================

ROOT_DIR = os.getcwd()

PYTHON_SCRIPTS = os.path.join(
    ROOT_DIR,
    "scripts",
    "python_scripts"
)

AVERAGE_SCRIPT = os.path.join(
    PYTHON_SCRIPTS,
    "average_analysis.py"
)

# Make analyses / averaging modules visible
os.environ["PYTHONPATH"] = (
    PYTHON_SCRIPTS
    + ":"
    + os.environ.get("PYTHONPATH", "")
)

# ==========================================================
# HELPERS
# ==========================================================

def run_average(name, std=False):

    command = [
        "python3",
        AVERAGE_SCRIPT,
        name,
        "-o",
        f"avg_{name}.dat"
    ]

    if std:
        command.append("--std")

    print(f"  [AVERAGE] {name}")

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        print(f"  [ERROR] {name}")

        if result.stderr:
            print(result.stderr)

        return False

    print("  [OK]")

    return True


# ==========================================================
# MAIN
# ==========================================================

print("")
print("==================================================")
print(" RUNNING AVERAGING")
print("==================================================")

# ----------------------------------------------------------
# MATRIX DATA
# ----------------------------------------------------------

if AVERAGING.get("msd_Li", False):
    run_average("msd_Li", std=True)

if AVERAGING.get("msd_Mn", False):
    run_average("msd_Mn", std=True)

if AVERAGING.get("msd_O", False):
    run_average("msd_O", std=True)

if AVERAGING.get("rdf_evolution", False):
    run_average("rdf_evolution")

if AVERAGING.get("coord_Mn", False):
    run_average("coord_Mn", std=True)

if AVERAGING.get("distortion", False):
    run_average("distortion", std=True)

if AVERAGING.get("energy", False):
    run_average("energy")

# ----------------------------------------------------------
# SPECIAL FILES
# ----------------------------------------------------------

if AVERAGING.get("diffusion", False):
    run_average("diffusion")

if AVERAGING.get("site_occupancy", False):
    run_average("site_occupancy")

if AVERAGING.get("jump_matrix", False):
    run_average("jump_matrix")

if AVERAGING.get("residence_time", False):
    run_average("residence_time")

# ----------------------------------------------------------
# XRD
# ----------------------------------------------------------

if AVERAGING.get("xrd", False):

    print("")
    print("[XRD] Searching XRD files")

    xrd_files = glob.glob(
        "Structure_1/xrd_*.dat"
    )

    xrd_names = []

    for filename in xrd_files:

        base = os.path.basename(filename)

        xrd_names.append(
            base.replace(".dat", "")
        )

    xrd_names = sorted(
        set(xrd_names)
    )

    for xrd_name in xrd_names:

        run_average(xrd_name)

# ==========================================================
# SUMMARY
# ==========================================================

print("")
print("==================================================")
print(" AVERAGING COMPLETE")
print("==================================================")
print("")

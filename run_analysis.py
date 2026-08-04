#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import shutil


from config.analysis_config import *

# ==========================================================
# PATHS
# ==========================================================

ROOT_DIR = os.getcwd()

SRC_DIR = os.path.join(
    ROOT_DIR,
    "src"
)

ANALYSIS_SCRIPT = os.path.join(
    SRC_DIR,
    "analysis.py"
)

AVERAGE_SCRIPT = os.path.join(
    SRC_DIR,
    "average_analysis.py"
)

os.environ["PYTHONPATH"] = (
    ROOT_DIR
    + ":"
    + os.environ.get("PYTHONPATH", "")
)

PLOT_SCRIPT = os.path.join(
    SRC_DIR,
    "plot.py"
)

# ==========================================================
# START
# ==========================================================

print("=" * 60)
print("START ANALYSIS PIPELINE")
print("=" * 60)

# ==========================================================
# LOOP OVER SYSTEMS
# ==========================================================

for system in SUB_WORK_DIR:

    system_path = os.path.join(
        ROOT_DIR,
        WORK_DIR,
        system
    )

    temp_dir = os.path.join(
        system_path,
        "TEMP"
    )

    if not os.path.isdir(temp_dir):

        print(
            f"[WARNING] {temp_dir} not found"
        )

        continue

    print("")
    print(f"[SYSTEM] {system}")

    os.chdir(temp_dir)

    # os.makedirs(
    #     DESTINATION_DIR,
    #     exist_ok=True
    # )

    # ======================================================
    # ANALYSIS
    # ======================================================

    print("")
    print("[STEP 1] ANALYSIS")

    for struct in sorted(
            os.listdir(".")):

        if (
            not struct.startswith(
                "Structure_"
            )
            or
            not os.path.isdir(struct)
        ):
            continue

        print(
            f"  [STRUCTURE] {struct}"
        )

        subprocess.run(
            [
                "python3",
                ANALYSIS_SCRIPT
            ],
            cwd=os.path.abspath(struct)
        )

    # ======================================================
    # AVERAGING
    # ======================================================

    print("")
    print("[STEP 2] AVERAGING")

    subprocess.run(
        [
            "python3",
            AVERAGE_SCRIPT
        ],
        cwd=temp_dir
    )

    # ======================================================
    # MOVE RESULTS
    # ======================================================

    print("")
    print("[STEP 3] MOVE RESULTS")

    destination = os.path.join(
        "..",
        DESTINATION_DIR
    )

    os.makedirs(
        destination,
        exist_ok=True
    )

    for file in os.listdir("."):

        if (
            file.startswith("avg_")
            and
            (
                file.endswith(".dat")
                or
                file.endswith(".png")
            )
        ):

            shutil.move(
                file,
                os.path.join(
                    destination,
                    file
                )
            )

        
    # ======================================================
    # STEP 4 : PLOTS
    # ======================================================
    
    print("")
    print("[STEP 4] GENERATING PLOTS")
    

    
    
    subprocess.run(
        [
            "python3",
            PLOT_SCRIPT
        ],
        cwd=destination
    )

    
    os.chdir(temp_dir)
    
    # ==========================================================
    # END
    # ==========================================================

print("")
print("=" * 60)
print("ALL SYSTEMS PROCESSED")
print("=" * 60)
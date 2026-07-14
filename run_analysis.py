#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import shutil

from scripts.config.analysis_config import *

ROOT_DIR = os.getcwd()

PYTHON_DIR = os.path.join(
    ROOT_DIR,
    "scripts",
    "python_scripts"
)

ANALYSIS_SCRIPT = os.path.join(
    PYTHON_DIR,
    "analysis.py"
)

AVERAGE_SCRIPT = os.path.join(
    PYTHON_DIR,
    "average_analysis.py"
)

os.environ["PYTHONPATH"] = (
    PYTHON_DIR
    + ":"
    + os.environ.get("PYTHONPATH", "")
)

print("=" * 60)
print("START ANALYSIS PIPELINE")
print("=" * 60)

for system in LI_DIRS:

    system_path = os.path.join(
        ROOT_DIR,
        LI_BASE,
        system
    )

    temp_dir = os.path.join(
        system_path,
        "TEMP"
    )

    if not os.path.isdir(temp_dir):

        print(
            f"[WARNING] {temp_dir} "
            "not found"
        )

        continue

    print("")
    print(f"[SYSTEM] {system}")

    os.chdir(temp_dir)

    os.makedirs(
        DESTINATION_DIR,
        exist_ok=True
    )

    # ==================================================
    # ANALYSIS
    # ==================================================

    for struct in sorted(
            os.listdir(".")):

        if not struct.startswith(
                "Structure_"):
            continue

        print(
            f"  [STRUCTURE] {struct}"
        )

        subprocess.run(
            [
                "python3",
                ANALYSIS_SCRIPT
            ],
            cwd=struct
        )

    # ==================================================
    # AVERAGING
    # ==================================================

    print("")
    print("[AVERAGING]")

    for data in DATA_TYPES:

        subprocess.run(
            [
                "python3",
                AVERAGE_SCRIPT,
                data,
                "-o",
                f"avg_{data}.dat"
            ]
        )

    # ==================================================
    # MOVE RESULTS
    # ==================================================

    destination = os.path.join(
        "..",
        DESTINATION_DIR
    )

    for file in os.listdir("."):

        if (
            file.endswith(".dat")
            or
            file.endswith(".png")
        ):

            shutil.move(
                file,
                os.path.join(
                    destination,
                    file
                )
            )

    os.chdir(ROOT_DIR)

print("")
print("=" * 60)
print("ALL SYSTEMS PROCESSED")
print("=" * 60)

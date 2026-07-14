#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


def extract_energy_from_log(
        logfile="log.lammps",
        step_min=10000,
        step_max=2010000,
        output_file="energy.dat"):

    print("")
    print("========================================")
    print(" ENERGY EXTRACTION")
    print("========================================")

    steps = []
    pe = []
    te = []

    reading = False
    columns = None

    with open(logfile, "r") as f:

        for line in f:

            words = line.split()

            if not words:
                continue

            if "Step" in words:

                if (
                    "PotEng" in words and
                    (
                        "TotEng" in words or
                        "Etot" in words
                    )
                ):

                    columns = words
                    reading = True

                continue

            if not reading:
                continue

            if words[0] == "Loop":

                reading = False
                continue

            try:

                step = int(
                    float(
                        words[
                            columns.index("Step")
                        ]
                    )
                )

                if (
                    step < step_min or
                    step > step_max
                ):
                    continue

                PE = float(
                    words[
                        columns.index("PotEng")
                    ]
                )

                if "TotEng" in columns:

                    TE = float(
                        words[
                            columns.index("TotEng")
                        ]
                    )

                else:

                    TE = float(
                        words[
                            columns.index("Etot")
                        ]
                    )

                steps.append(step)
                pe.append(PE)
                te.append(TE)

            except Exception:
                pass

    data = np.column_stack(
        (steps, pe, te)
    )

    np.savetxt(
        output_file,
        data,
        header="Step PE TE"
    )

    print(
        f"Saved {len(steps)} entries "
        f"to {output_file}"
    )

    return (
        np.array(steps),
        np.array(

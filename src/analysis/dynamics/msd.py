#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from MDAnalysis.analysis.msd import EinsteinMSD


def compute_msd_and_diff(
        u,
        time,
        selection,
        label):

    print(f"Computing MSD for {label}...")

    msd = EinsteinMSD(
        u,
        select=selection,
        msd_type="xyz"
    )

    msd.run()

    values = msd.results.timeseries

    start = int(0.3 * len(time))
    end = int(0.8 * len(time))

    slope = np.polyfit(
        time[start:end],
        values[start:end],
        1
    )[0]

    diffusion = slope / 6.0

    print(
        f"{label} diffusion = "
        f"{diffusion:.3e}"
    )

    np.savetxt(
        f"msd_{label}.dat",
        np.column_stack([time, values]),
        header="Time(ps) MSD(A2)"
    )

    return diffusion


def run_msd_analysis(
        u,
        time,
        species):

    diffusion_results = {}

    for label, selection in species.items():

        diffusion_results[label] = (
            compute_msd_and_diff(
                u,
                time,
                selection,
                label
            )
        )

    with open("diffusion.dat", "w") as f:

        f.write("# Species Diffusion\n")

        for label, value in diffusion_results.items():

            f.write(
                f"{label} "
                f"{value:.8e}\n"
            )

    return diffusion_results

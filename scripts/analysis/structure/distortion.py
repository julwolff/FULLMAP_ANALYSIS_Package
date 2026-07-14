#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from MDAnalysis.analysis import distances


def compute_distortion(
        u,
        center_selection="type 2",
        oxygen_selection="type 3",
        cutoff=2.5):

    print("Computing Mn-O distortion...")

    centers = u.select_atoms(
        center_selection
    )

    oxygens = u.select_atoms(
        oxygen_selection
    )

    distortions = []

    for ts in u.trajectory:

        frame_dist = []

        for atom in centers:

            d = distances.distance_array(
                atom.position.reshape(1, 3),
                oxygens.positions,
                box=u.dimensions
            )[0]

            neigh = d[d < cutoff]

            if len(neigh) < 2:
                continue

            mean_d = np.mean(neigh)

            distortion = np.sqrt(
                np.mean(
                    (neigh - mean_d) ** 2
                )
            )

            frame_dist.append(
                distortion
            )

        if len(frame_dist) == 0:
            distortions.append(0.0)
        else:
            distortions.append(
                np.mean(frame_dist)
            )

    distortions = np.array(
        distortions
    )

    time = np.arange(
        len(distortions)
    )

    np.savetxt(
        "distortion.dat",
        np.column_stack(
            [time, distortions]
        ),
        header="Frame Distortion"
    )

    return 

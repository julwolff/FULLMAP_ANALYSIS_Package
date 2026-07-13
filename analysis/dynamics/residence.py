#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


def compute_residence_times(
        assignment_file="site_assignment.dat",
        timestep_ps=0.020):

    print("Computing residence times...")

    data = np.loadtxt(
        assignment_file,
        comments="#",
        dtype=str
    )

    frames = data[:, 0].astype(int)
    atomids = data[:, 1].astype(int)
    sites = data[:, 3]

    residence = {}

    for atom in np.unique(atomids):

        mask = atomids == atom

        atom_frames = frames[mask]
        atom_sites = sites[mask]

        order = np.argsort(atom_frames)

        atom_frames = atom_frames[order]
        atom_sites = atom_sites[order]

        current_site = atom_sites[0]
        length = 1

        for i in range(1, len(atom_sites)):

            if atom_sites[i] == current_site:

                length += 1

            else:

                residence.setdefault(
                    current_site,
                    []
                ).append(length)

                current_site = atom_sites[i]
                length = 1

        residence.setdefault(
            current_site,
            []
        ).append(length)

    with open(
            "residence_time.dat",
            "w") as f:

        f.write(
            "# Site Tau(ps)\n"
        )

        for site, lengths in sorted(
                residence.items()):

            tau = (
                np.mean(lengths)
                * timestep_ps
            )

            f.write(
                f"{site} "
                f"{tau:.6f}\n"
            )

    print(
        f"Computed residence times "
        f"for {len(residence)} sites"
    )

    return residence

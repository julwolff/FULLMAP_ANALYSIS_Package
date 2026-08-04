#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


def compute_jumps(
        assignment_file="site_assignment.dat"):

    print("Computing jumps...")

    data = np.loadtxt(
        assignment_file,
        comments="#",
        dtype=str
    )

    frames = data[:, 0].astype(int)
    atomids = data[:, 1].astype(int)
    elements = data[:, 2]
    sites = data[:, 3]

    jumps = []
    matrix = {}

    for atom in np.unique(atomids):

        mask = atomids == atom

        atom_frames = frames[mask]
        atom_sites = sites[mask]
        atom_element = elements[mask][0]

        order = np.argsort(atom_frames)

        atom_frames = atom_frames[order]
        atom_sites = atom_sites[order]

        for i in range(len(atom_sites) - 1):

            old_site = atom_sites[i]
            new_site = atom_sites[i + 1]

            if old_site == new_site:
                continue

            frame = atom_frames[i + 1]

            jumps.append(
                [
                    frame,
                    atom,
                    atom_element,
                    old_site,
                    new_site
                ]
            )

            key = (
                old_site,
                new_site
            )

            matrix[key] = (
                matrix.get(key, 0) + 1
            )

    with open("jumps.dat", "w") as f:

        f.write(
            "# Frame AtomID Element "
            "FromSite ToSite\n"
        )

        for row in jumps:

            f.write(
                f"{row[0]} "
                f"{row[1]} "
                f"{row[2]} "
                f"{row[3]} "
                f"{row[4]}\n"
            )

    with open("jump_matrix.dat", "w") as f:

        f.write(
            "# FromSite ToSite Count\n"
        )

        for key, count in sorted(
                matrix.items()):

            f.write(
                f"{key[0]} "
                f"{key[1]} "
                f"{count}\n"
            )

    print(
        f"Detected {len(jumps)} jumps"
    )

    return jumps, matrix

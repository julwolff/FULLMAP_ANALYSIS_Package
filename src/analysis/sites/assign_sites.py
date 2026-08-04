#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


def assign_sites(
        atom_position,
        site_positions):
    """
    Return the index of the closest site.
    """

    distances = np.linalg.norm(
        site_positions - atom_position,
        axis=1
    )

    return np.argmin(distances)


def assign_sites_trajectory(
        u,
        sites_file="sites.dat",
        output_file="site_assignment.dat"):

    print("")
    print("========================================")
    print(" SITE ASSIGNMENT")
    print("========================================")

    print(f"Reading site file: {sites_file}")

    sites = np.loadtxt(
        sites_file,
        comments="#",
        dtype=str
    )

    site_ids = (
        sites[:, 0].astype(int)
    )

    elements = sites[:, 1]

    coords = (
        sites[:, 3:6].astype(float)
    )

    n_sites = len(site_ids)

    n_li_sites = np.sum(
        elements == "Li"
    )

    n_mn_sites = np.sum(
        elements == "Mn"
    )

    print("")
    print("Loaded site information:")
    print(f"  Total sites : {n_sites}")
    print(f"  Li sites    : {n_li_sites}")
    print(f"  Mn sites    : {n_mn_sites}")

    n_frames = len(u.trajectory)

    print("")
    print(f"Trajectory contains {n_frames} frames")

    assignment_count = 0

    with open(output_file, "w") as f:

        f.write(
            "# Frame AtomID Element SiteID\n"
        )

        for iframe, ts in enumerate(
                u.trajectory):

            if (
                iframe % 100 == 0
                or
                iframe == n_frames - 1
            ):

                print(
                    f"Processing frame "
                    f"{iframe + 1}/{n_frames}"
                )

            frame_assignments = 0

            for atom in u.atoms:

                symbol = {
                    1: "Li",
                    2: "Mn",
                    3: "O"
                }.get(int(atom.type))

                if symbol not in [
                        "Li",
                        "Mn"]:
                    continue

                mask = (
                    elements == symbol
                )

                local_sites = coords[
                    mask
                ]

                local_ids = site_ids[
                    mask
                ]

                distances = np.linalg.norm(
                    local_sites -
                    atom.position,
                    axis=1
                )

                site = local_ids[
                    np.argmin(distances)
                ]

                f.write(
                    f"{iframe} "
                    f"{atom.id} "
                    f"{symbol} "
                    f"{site}\n"
                )

                frame_assignments += 1
                assignment_count += 1

            if (
                iframe % 100 == 0
                or
                iframe == n_frames - 1
            ):

                print(
                    f"  Assigned "
                    f"{frame_assignments} atoms"
                )

    print("")
    print("Assignment completed")
    print("--------------------")
    print(
        f"Total assignments : "
        f"{assignment_count}"
    )

    print(
        f"Output file       : "
        f"{output_file}"
    )

    print("========================================")
    print("")

    return assignment_count
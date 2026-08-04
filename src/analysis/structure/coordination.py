#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from MDAnalysis.analysis import distances


def compute_coordination(
        u,
        center_selection="Mn",
        neighbor_selection="O",
        cutoff=2.5):
    """
    Compute the average coordination number
    of center atoms with respect to neighbors.

    Example:
        Mn-O coordination

    Parameters
    ----------
    u : MDAnalysis Universe

    center_selection : str
        Atom selection for the center atoms.

    neighbor_selection : str
        Atom selection for neighboring atoms.

    cutoff : float
        Distance cutoff in Angstrom.

    Returns
    -------
    coordination : np.ndarray
        Average coordination number at each frame.
    """

    print("Computing coordination...")

    centers = u.select_atoms(
        center_selection
    )

    neighbors = u.select_atoms(
        neighbor_selection
    )

    coordination = []

    for ts in u.trajectory:

        cn_total = 0

        for atom in centers:

            d = distances.distance_array(
                atom.position.reshape(1, 3),
                neighbors.positions,
                box=u.dimensions
            )[0]

            cn_total += np.sum(
                d < cutoff
            )

        cn_average = (
            cn_total / len(centers)
        )

        coordination.append(
            cn_average
        )

    coordination = np.array(
        coordination
    )

    time = np.arange(
        len(coordination)
    )

    np.savetxt(
        "coord_Mn.dat",
        np.column_stack(
            [time, coordination]
        ),
        header="Frame Coordination"
    )

    print(
        f"Saved coord_Mn.dat "
        f"({len(coordination)} frames)"
    )

    return coordination


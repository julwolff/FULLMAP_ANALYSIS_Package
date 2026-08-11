#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 11:01:01 2026

@author: jwjules
"""

import numpy as np
from pymatgen.core import Structure


def check_cell(cif_file, u):

    structure = Structure.from_file(cif_file)

    cif_cell = np.array([
        structure.lattice.a,
        structure.lattice.b,
        structure.lattice.c,
        structure.lattice.alpha,
        structure.lattice.beta,
        structure.lattice.gamma
    ])

    ts = u.trajectory[0]

    traj_cell = np.array(ts.dimensions)

    print("")
    print("========================================")
    print("CELL COMPARISON")
    print("========================================")

    labels = [
        "a", "b", "c",
        "alpha", "beta", "gamma"
    ]

    for label, cif, traj in zip(
        labels,
        cif_cell,
        traj_cell
    ):

        difference = traj - cif

        print(
            f"{label:5s} "
            f"CIF = {cif:12.6f}   "
            f"Trajectory = {traj:12.6f}   "
            f"Difference = {difference:+.6e}"
        )

    if np.allclose(
        cif_cell,
        traj_cell,
        atol=1e-5
    ):
        print("")
        print("✓ Cells are consistent")

    else:
        print("")
        print("✗ WARNING: Cells are different")
        
        
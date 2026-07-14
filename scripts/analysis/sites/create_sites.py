#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from itertools import combinations

from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import (
    SpacegroupAnalyzer
)


def find_tetrahedral_sites(
        O_positions,
        oo_cutoff=4.0,
        merge_cutoff=0.5):

    print("Searching tetrahedral sites...")

    candidates = []

    for tetra in combinations(
            range(len(O_positions)),
            4):

        coords = O_positions[list(tetra)]

        distances = []

        for i in range(4):
            for j in range(i + 1, 4):

                distances.append(
                    np.linalg.norm(
                        coords[i] - coords[j]
                    )
                )

        distances = np.array(
            distances
        )

        if np.max(distances) > oo_cutoff:
            continue

        if np.std(distances) > 0.5:
            continue

        candidates.append(
            np.mean(coords, axis=0)
        )

    unique = []

    for site in candidates:

        if len(unique) == 0:

            unique.append(site)
            continue

        d = np.linalg.norm(
            np.array(unique) - site,
            axis=1
        )

        if np.min(d) > merge_cutoff:

            unique.append(site)

    return np.array(unique)


def create_sites_file(
        cif_file,
        output_file="sites.dat",
        elements=("Li", "Mn")):

    structure = Structure.from_file(
        cif_file
    )

    oxygen_positions = np.array([
        s.coords
        for s in structure
        if s.specie.symbol == "O"
    ])

    th_sites = find_tetrahedral_sites(
        oxygen_positions
    )

    sga = SpacegroupAnalyzer(
        structure
    )

    symm = (
        sga.get_symmetrized_structure()
    )

    site_id = 0

    with open(output_file, "w") as f:

        f.write(
            "# SiteID Element Label x y z\n"
        )

        for wyckoff, indices in zip(
                symm.wyckoff_symbols,
                symm.equivalent_indices):

            for idx in indices:

                site = symm[idx]

                element = (
                    site.specie.symbol
                )

                if element not in elements:
                    continue

                x, y, z = (
                    site.frac_coords
                )

                f.write(
                    f"{site_id} "
                    f"{element} "
                    f"{wyckoff} "
                    f"{x:.8f} "
                    f"{y:.8f} "
                    f"{z:.8f}\n"
                )

                site_id += 1

        for pos in th_sites:

            f.write(
                f"{site_id} "
                f"Li "
                f"TH "
                f"{pos.8f} "
                f"{pos.8f} "
                f"{pos.8f}\n"
            )

            site_id += 1

    print(
        f"{site_id} sites saved "
        f"to {output_file}"
    )

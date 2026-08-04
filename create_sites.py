#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from itertools import combinations

from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import (
    SpacegroupAnalyzer
)


from itertools import combinations
from math import comb

import numpy as np


def find_tetrahedral_sites(
        O_positions,
        oo_cutoff=4.0,
        merge_cutoff=0.5):

    print("")
    print("========================================")
    print(" TETRAHEDRAL SITE SEARCH")
    print("========================================")

    n_oxygen = len(O_positions)

    print(
        f"Number of oxygen atoms : "
        f"{n_oxygen}"
    )

    n_candidates = comb(
        n_oxygen,
        4
    )

    print("")
    print(
        f"Possible O4 combinations : "
        f"{n_candidates:,}"
    )

    if n_candidates > 1e6:

        print("")
        print("WARNING")
        print("-------")

        print(
            "More than one million "
            "tetrahedra will be tested."
        )

        print(
            "Execution may become slow."
        )

    print("")
    print("Search parameters")
    print("-----------------")

    print(
        f"O-O cutoff    : "
        f"{oo_cutoff:.2f} Å"
    )

    print(
        f"Merge cutoff  : "
        f"{merge_cutoff:.2f} Å"
    )

    print("")
    print("Starting tetrahedron search...")
    print("")

    candidates = []

    tested = 0

    rejected_distance = 0
    rejected_distortion = 0

    accepted = 0

    progress_interval = max(
        1,
        n_candidates // 20000
    )

    for tetra in combinations(
            range(n_oxygen),
            4):

        tested += 1

        if (
            tested % progress_interval == 0
        ):

            percentage = (
                100.0 *
                tested /
                n_candidates
            )

            print(
                f"Progress : "
                f"{percentage:6.2f}% "
                f"({tested:,}/"
                f"{n_candidates:,})"
            )

        coords = O_positions[
            list(tetra)
        ]

        distances = []

        for i in range(4):
            for j in range(
                    i + 1,
                    4):

                distances.append(
                    np.linalg.norm(
                        coords[i]
                        -
                        coords[j]
                    )
                )

        distances = np.array(
            distances
        )

        if np.max(
                distances
        ) > oo_cutoff:

            rejected_distance += 1
            continue

        if np.std(
                distances
        ) > 0.5:

            rejected_distortion += 1
            continue

        center = np.mean(
            coords,
            axis=0
        )

        candidates.append(
            center
        )

        accepted += 1

    print("")
    print("Raw tetrahedron search completed")
    print("================================")

    print(
        f"Tested tetrahedra      : "
        f"{tested:,}"
    )

    print(
        f"Rejected (distance)   : "
        f"{rejected_distance:,}"
    )

    print(
        f"Rejected (distortion) : "
        f"{rejected_distortion:,}"
    )

    print(
        f"Accepted candidates   : "
        f"{accepted:,}"
    )

    print("")
    print(
        "Removing duplicated "
        "tetrahedral centers..."
    )

    unique = []

    duplicates_removed = 0

    for site in candidates:

        if len(unique) == 0:

            unique.append(site)
            continue

        d = np.linalg.norm(
            np.array(unique)
            -
            site,
            axis=1
        )

        if np.min(d) > merge_cutoff:

            unique.append(site)

        else:

            duplicates_removed += 1

    print("")
    print("Duplicate removal summary")
    print("-------------------------")

    print(
        f"Duplicates removed : "
        f"{duplicates_removed:,}"
    )

    print(
        f"Final TH sites     : "
        f"{len(unique):,}"
    )

    print("")
    print("========================================")
    print("")

    return np.array(unique)


def create_sites_file(
        cif_file,
        output_file="sites.dat",
        elements=("Li", "Mn")):

    print("")
    print("========================================")
    print(" SITE GENERATION")
    print("========================================")

    print(f"Reading CIF : {cif_file}")

    structure = Structure.from_file(
        cif_file
    )

    print("")
    print("Structure summary")
    print("-----------------")
    print(
        f"Total atoms : "
        f"{len(structure)}"
    )

    species = {}

    for site in structure:

        symbol = site.specie.symbol

        species[symbol] = (
            species.get(symbol, 0) + 1
        )

    for symbol, count in species.items():

        print(
            f"  {symbol:<3} : {count}"
        )

    oxygen_positions = np.array([
        s.coords
        for s in structure
        if s.specie.symbol == "O"
    ])

    print("")
    print(
        f"Number of O atoms : "
        f"{len(oxygen_positions)}"
    )
    
    print("")
    print("Performing symmetry analysis...")

    sga = SpacegroupAnalyzer(
        structure
    )

    symm = (
        sga.get_symmetrized_structure()
    )

    site_id = 0

    n_li = 0
    n_mn = 0

    print("")
    print("Symmetry analysis")
    print("-----------------")
    
    spacegroup_symbol = sga.get_space_group_symbol()
    spacegroup_number = sga.get_space_group_number()
    
    print(
        f"Space group : "
        f"{spacegroup_symbol}"
    )
    
    print(
        f"Space group number : "
        f"{spacegroup_number}"
        )

    th_sites = find_tetrahedral_sites(
        oxygen_positions
    )






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
                f"{pos[0]:.8f} "
                f"{pos[1]:.8f} "
                f"{pos[2]:.8f}\n"
            )

            site_id += 1

    print(
        f"{site_id} sites saved "
        f"to {output_file}"
    )

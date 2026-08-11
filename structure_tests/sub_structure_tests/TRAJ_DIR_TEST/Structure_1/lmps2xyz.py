#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 09:00:19 2026

@author: jwjules
"""

#!/usr/bin/env python3

import sys
from pathlib import Path


def pdb_to_xyz(input_file, replacements):

    input_path = Path(input_file)

    # Output filename
    output_path = input_path.with_suffix(".xyz")

    atoms = []

    with open(input_path, "r") as f:

        for line in f:

            # Only read ATOM/HETATM records
            if not line.startswith(("ATOM", "HETATM")):
                continue

            # LAMMPS atom type: columns 13-16
            atom_type = line[12:16].strip()

            try:
                type_number = int(atom_type)
                element = replacements[type_number - 1]
            except (ValueError, IndexError):
                print(
                    f"Warning: unknown atom type '{atom_type}', "
                    f"skipping line."
                )
                continue

            # PDB coordinates:
            # X = columns 31-38
            # Y = columns 39-46
            # Z = columns 47-54
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])

            atoms.append((element, x, y, z))

    # Write XYZ
    with open(output_path, "w") as f:

        # Number of atoms
        f.write(f"{len(atoms)}\n")

        # Comment line
        f.write(f"Converted from {input_path.name}\n")

        # Atoms
        for element, x, y, z in atoms:
            f.write(
                f"{element:<2} "
                f"{x:12.6f} "
                f"{y:12.6f} "
                f"{z:12.6f}\n"
            )

    print(f"Input : {input_path}")
    print(f"Output: {output_path}")
    print(f"Atoms : {len(atoms)}")

    print("Mapping:")
    for i, element in enumerate(replacements, start=1):
        print(f"  type {i} -> {element}")


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print(
            "Usage:\n"
            "  python pdb_to_xyz.py input.pdb Element1 Element2 ...\n\n"
            "Example:\n"
            "  python pdb_to_xyz.py exemple.pdb Li Mn O"
        )
        sys.exit(1)

    input_file = sys.argv[1]
    replacements = sys.argv[2:]

    pdb_to_xyz(input_file, replacements)
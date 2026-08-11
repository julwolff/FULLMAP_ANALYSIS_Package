#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 08:57:26 2026

@author: jwjules
"""

#!/usr/bin/env python3

import sys
from pathlib import Path


def convert_pdb(input_file, replacements):
    input_path = Path(input_file)

    # Output filename
    output_path = input_path.with_name(
        input_path.stem + "_converted.pdb"
    )

    with open(input_path, "r") as fin, open(output_path, "w") as fout:

        for line in fin:

            # Only modify ATOM/HETATM records
            if line.startswith(("ATOM", "HETATM")):

                # LAMMPS atom type is in columns 13-16 in your file
                atom_type = line[12:16].strip()

                # Convert type number to element
                try:
                    type_number = int(atom_type)
                    element = replacements[type_number - 1]
                except (ValueError, IndexError):
                    fout.write(line)
                    continue

                # Replace atom name (columns 13-16)
                line = (
                    line[:12]
                    + f"{element:>4}"
                    + line[16:]
                )

                # Replace residue name (columns 18-20)
                line = (
                    line[:17]
                    + f"{element:>3}"
                    + line[20:]
                )

                # Replace element field at the end of the PDB line
                # PDB element field = columns 77-78
                line = line.rstrip("\n").ljust(78)
                line = line[:76] + f"{element:>2}" + line[78:] + "\n"

            fout.write(line)

    print(f"Input : {input_path}")
    print(f"Output: {output_path}")
    print("Mapping:")

    for i, element in enumerate(replacements, start=1):
        print(f"  type {i} -> {element}")


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print(
            "Usage:\n"
            "  python script.py input.pdb Element1 Element2 Element3 ...\n\n"
            "Example:\n"
            "  python script.py exemple.pdb Li Mn O"
        )
        sys.exit(1)

    input_file = sys.argv[1]
    replacements = sys.argv[2:]

    convert_pdb(input_file, replacements)
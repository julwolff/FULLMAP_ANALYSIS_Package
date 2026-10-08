#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:56:35 2026

@author: jwjules
"""



from collections import defaultdict
import numpy as np


def accumulate_local_structures(
        file_list,
        output_file):

    structure_counts = defaultdict(int)

    for filename in file_list:

        table = np.loadtxt(
            filename,
            comments="#",
            dtype=str,
            skiprows=1
        )

        # Handle files containing only one structure
        if table.ndim == 1:
            table = table.reshape(1, -1)

        for row in table:

            structure = row[0]
            count = int(row[1])

            structure_counts[
                structure
            ] += count

    with open(output_file, "w") as f:

        f.write(
            "Structure Count\n"
        )

        for structure in sorted(
                structure_counts.keys()):

            f.write(
                f"{structure} "
                f"{structure_counts[structure]}\n"
            )
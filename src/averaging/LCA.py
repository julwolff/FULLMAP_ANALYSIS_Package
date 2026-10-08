#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:56:35 2026

@author: jwjules
"""

from collections import defaultdict
from math import gcd
from functools import reduce
import re
import numpy as np


def reduce_formula(formula):
    """
    Reduce a chemical formula to its simplest integer ratio.

    Examples
    --------
    Li4Mn2O8 -> Li2Mn1O4
    Li2Mn2O6 -> Li1Mn1O3
    Li5Mn2O7 -> Li5Mn2O7
    """

    elements = re.findall(
        r"([A-Z][a-z]*)(\d+)",
        formula
    )

    if not elements:
        return formula

    counts = [
        int(count)
        for _, count in elements
    ]

    common_divisor = reduce(
        gcd,
        counts
    )

    reduced_formula = ""

    for element, count in elements:

        count = int(count)

        reduced_count = count // common_divisor

        reduced_formula += (
            f"{element}{reduced_count}"
        )

    return reduced_formula

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

        if table.ndim == 1:
            table = table.reshape(1, -1)

        for row in table:

            structure = row[0]
            count = int(row[1])

            # Reduce stoichiometric ratio
            structure = reduce_formula(
                structure
            )

            # Accumulate reduced structures
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
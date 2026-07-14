#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import numpy as np


def accumulate_jump_matrix(
        file_list,
        output_file):

    jump_counts = defaultdict(int)

    for filename in file_list:

        table = np.loadtxt(
            filename,
            comments="#",
            dtype=str
        )

        for row in table:

            source = row[0]
            target = row[1]
            count = int(row[2])

            jump_counts[
                (source, target)
            ] += count

    with open(output_file, "w") as f:

        f.write(
            "# FromSite ToSite Count\n"
        )

        for key in sorted(
                jump_counts.keys()):

            f.write(
                f"{key[0]} "
                f"{key[1]} "
                f"{jump_counts[key]}\n"
            )

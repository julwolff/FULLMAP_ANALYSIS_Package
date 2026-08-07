#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 15:55:12 2026

@author: jwjules
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


def average_site_occupancy(
        file_list,
        output_file):

    occupancy = {}

    for filename in file_list:

        table = np.loadtxt(
            filename,
            comments="#",
            dtype=str
        )

        frames = np.unique(
            table[:, 0].astype(int)
        )

        for frame in frames:

            mask = (
                table[:, 0].astype(int)
                == frame
            )

            data = table[mask]

            n_li_li = 0
            n_li_mn = 0
            n_mn_li = 0
            n_mn_mn = 0

            for row in data:

                atom_type = row[2]
                site_type = row[4]

                if (
                    atom_type == "Li"
                    and
                    site_type == "Li"
                ):
                    n_li_li += 1

                elif (
                    atom_type == "Li"
                    and
                    site_type == "Mn"
                ):
                    n_li_mn += 1

                elif (
                    atom_type == "Mn"
                    and
                    site_type == "Li"
                ):
                    n_mn_li += 1

                elif (
                    atom_type == "Mn"
                    and
                    site_type == "Mn"
                ):
                    n_mn_mn += 1

            if frame not in occupancy:

                occupancy[frame] = np.zeros(
                    4,
                    dtype=int
                )

            occupancy[frame] += np.array(
                [
                    n_li_li,
                    n_li_mn,
                    n_mn_li,
                    n_mn_mn
                ]
            )

    with open(output_file, "w") as f:

        f.write(
            "# Frame "
            "NLiatomsinLiSites "
            "NLiatomsinMnSites "
            "NMnatomsinLiSites "
            "NMnatomsinMnSites\n"
        )

        for frame in sorted(
                occupancy.keys()):

            values = occupancy[frame]

            f.write(
                f"{frame} "
                f"{values[0]} "
                f"{values[1]} "
                f"{values[2]} "
                f"{values[3]}\n"
            )
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


def average_diffusion(
        file_list,
        output_file):

    species_data = {}

    for filename in file_list:

        with open(filename) as f:

            for line in f:

                if line.startswith("#"):
                    continue

                fields = line.split()

                if len(fields) != 2:
                    continue

                species = fields[0]
                value = float(fields[1])

                species_data.setdefault(
                    species,
                    []
                ).append(value)

    with open(output_file, "w") as f:

        f.write(
            "# Species Mean Std\n"
        )

        for species in sorted(
                species_data.keys()):

            values = np.array(
                species_data[species]
            )

            f.write(
                f"{species} "
                f"{np.mean(values):.8e} "
                f"{np.std(values):.8e}\n"
            )

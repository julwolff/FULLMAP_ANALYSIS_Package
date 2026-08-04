#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


def average_residence_time(
        file_list,
        output_file):

    data = {}

    for filename in file_list:

        table = np.loadtxt(
            filename,
            comments="#",
            dtype=str
        )

        for row in table:

            site = row[0]
            tau = float(row[1])

            data.setdefault(
                site,
                []
            ).append(tau)

    with open(output_file, "w") as f:

        f.write(
            "# SiteID MeanTau StdTau\n"
        )

        for site in sorted(
                data.keys(),
                key=int):

            values = np.array(
                data[site]
            )

            f.write(
                f"{site} "
                f"{np.mean(values):.6f} "
                f"{np.std(values):.6f}\n"
            )

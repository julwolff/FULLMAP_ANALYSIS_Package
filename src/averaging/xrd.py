#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


def average_xrd(
        file_list,
        output_file):

    data = [
        np.loadtxt(f)
        for f in file_list
    ]

    theta = data[0][:, 0]

    intensities = np.stack(
        [x[:, 1] for x in data]
    )

    mean = np.mean(
        intensities,
        axis=0
    )

    std = np.std(
        intensities,
        axis=0
    )

    result = np.column_stack(
        [
            theta,
            mean,
            std
        ]
    )

    np.savetxt(
        output_file,
        result,
        header="2theta MeanIntensity StdIntensity"
    )

    return result

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


def average_matrix(
        file_list,
        output_file,
        compute_std=False):

    matrices = [
        np.loadtxt(f)
        for f in file_list
    ]

    stack = np.stack(matrices)

    mean = np.mean(
        stack,
        axis=0
    )

    if compute_std:

        std = np.std(
            stack,
            axis=0
        )

        result = np.column_stack(
            [
                mean[:, 0],
                mean[:, 1],
                std[:, 1]
            ]
        )

        np.savetxt(
            output_file,
            result,
            header="X Mean Std"
        )

        return result

    np.savetxt(
        output_file,
        mean
    )

    return mean

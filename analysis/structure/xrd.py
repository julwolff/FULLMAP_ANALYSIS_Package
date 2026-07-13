#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from pymatgen.core import Lattice
from pymatgen.core import Structure
from pymatgen.analysis.diffraction.xrd import (
    XRDCalculator
)

from scipy.interpolate import interp1d

from MDAnalysis.lib.mdamath import (
    triclinic_vectors
)


def compute_xrd_series(
        u,
        wavelength="CuKa",
        twotheta_min=10,
        twotheta_max=90,
        dump_every=1000,
        xrd_every=200000,
        xrd_window=20000):

    print("Computing XRD series...")

    calculator = XRDCalculator(
        wavelength=wavelength
    )

    type_map = {
        1: "Li",
        2: "Mn",
        3: "O"
    }

    total_steps = (
        len(u.trajectory) - 1
    ) * dump_every

    centers = np.arange(
        xrd_every,
        total_steps + xrd_every,
        xrd_every
    )

    twotheta_grid = np.linspace(
        twotheta_min,
        twotheta_max,
        4000
    )

    for center in centers:

        print(

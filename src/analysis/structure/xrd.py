#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from pymatgen.core import Lattice
from pymatgen.core import Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator

from scipy.interpolate import interp1d

from MDAnalysis.lib.mdamath import triclinic_vectors


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
            f"XRD around step {center}"
        )

        start_step = (
            center - xrd_window // 2
        )

        end_step = (
            center + xrd_window // 2
        )

        start_frame = max(
            0,
            start_step // dump_every
        )

        end_frame = min(
            len(u.trajectory) - 1,
            end_step // dump_every
        )

        intensity_sum = np.zeros_like(
            twotheta_grid
        )

        nframes = 0

        for iframe in range(
                start_frame,
                end_frame + 1):

            u.trajectory[iframe]

            lattice = Lattice(
                triclinic_vectors(
                    u.dimensions
                )
            )
            
            
            species = [
                type_map[int(a.type)]
                for a in u.atoms
            ]
            
            
            coords = (
                u.atoms.positions
            )

            structure = Structure(
                lattice,
                species,
                coords,
                coords_are_cartesian=True
            )

            pattern = (
                calculator.get_pattern(
                    structure,
                    two_theta_range=(
                        twotheta_min,
                        twotheta_max
                    )
                )
            )

            interp = interp1d(
                pattern.x,
                pattern.y,
                bounds_error=False,
                fill_value=0.0
            )

            intensity_sum += interp(
                twotheta_grid
            )

            nframes += 1

        if nframes == 0:
            continue

        intensity = (
            intensity_sum / nframes
        )

        if intensity.max() > 0:
            intensity /= intensity.max()

        np.savetxt(
            f"xrd_{center}.dat",
            np.column_stack(
                [
                    twotheta_grid,
                    intensity
                ]
            ),
            header="2theta Intensity"
        )

        print(
            f"Saved xrd_{center}.dat"
        )
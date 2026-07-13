#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 15:17:30 2026

@author: jwjules
"""

import numpy as np
import glob
import argparse
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ================================
# ARGUMENTS
# ================================

parser = argparse.ArgumentParser(
    description="Average data from Structure_X folders (matrix-based)"
)

parser.add_argument("name", help="Name of the .dat file")
parser.add_argument("-o", "--output", default=None)
parser.add_argument("--std", action="store_true",
                    help="Compute std (only for 2-column data)")

args = parser.parse_args()

NAME = args.name
OUTPUT = args.output if args.output else NAME + ".dat"
COMPUTE_STD = args.std

# ================================
# FILE DISCOVERY
# ================================

files = sorted(glob.glob(f"Structure_*/{NAME}.dat"))

if len(files) == 0:
    print(f"[ERROR] No files found for {NAME}")
    sys.exit(1)

print(f"[INFO] Found {len(files)} files for {NAME}")

# ================================
# CORE FUNCTION
# ================================

def average_matrices(file_list, compute_std=False):
    """
    Average a list of matrices with shape [n_points, n_cols]

    Returns:
        x                : axis
        mean_values      : averaged data
        std_values       : standard deviation (or None)
    """

    matrices = []

    for f in file_list:
        try:
            data = np.loadtxt(f)
            matrices.append(data)
        except Exception as e:
            print(f"[WARNING] Skipping {f}: {e}")

    if len(matrices) == 0:
        raise ValueError("No valid data files")

    matrices = np.array(matrices)

    # shape check
    if matrices.ndim != 3:
        raise ValueError("Data must be 3D (n_struct, n_points, n_cols)")

    n_struct, n_points, n_cols = matrices.shape

    # consistency check
    lengths = [m.shape[0] for m in matrices]
    if len(set(lengths)) != 1:
        raise ValueError("Inconsistent number of points across files")

    # axis
    x = matrices[0, :, 0]

    # values (exclude column 0)
    values = matrices[:, :, 1:]

    mean_vals = np.mean(values, axis=0)

    if compute_std:
        std_vals = np.std(values, axis=0)
    else:
        std_vals = None

    return x, mean_vals, std_vals


# ================================
# SPECIAL CASE: DIFFUSION
# ================================

if NAME == "diffusion":

    print("[INFO] Processing diffusion")

    data = {}

    for f in files:
        try:
            with open(f) as ff:
                for line in ff:
                    if line.startswith("#") or not line.strip():
                        continue
                    sp, val = line.split()
                    data.setdefault(sp, []).append(float(val))
        except Exception as e:
            print(f"[WARNING] Skipping {f}: {e}")

    if not data:
        print("[ERROR] No valid diffusion data")
        sys.exit(1)

    with open(OUTPUT, "w") as out:
        out.write("# Species Mean Std\n")

        for sp, vals in data.items():
            vals = np.array(vals)
            out.write(f"{sp} {vals.mean():.6e} {vals.std():.6e}\n")

    # plot
    try:
        plt.figure()
        species = list(data.keys())
        means = [np.mean(data[s]) for s in species]
        stds = [np.std(data[s]) for s in species]

        plt.bar(species, means, yerr=stds)
        plt.ylabel("Diffusion coefficient")
        plt.title("Diffusion comparison")
        plt.savefig(NAME + ".png")
        plt.close()
    except Exception as e:
        print(f"[WARNING] Plot failed: {e}")

    print("✅ diffusion done")
    sys.exit(0)

# ================================
# GENERAL MATRIX AVERAGING
# ================================

try:
    sample = np.loadtxt(files[0])
    n_cols = sample.shape[1]

    # ✅ RULE:
    # STD only for 2-column data AND not RDF
    if n_cols == 2 and NAME != "rdf_evolution":
        use_std = COMPUTE_STD
    else:
        use_std = False

    x, mean_vals, std_vals = average_matrices(files, use_std)

except Exception as e:
    print(f"[ERROR] Averaging failed: {e}")
    sys.exit(1)

# ================================
# SAVE
# ================================

try:

    if std_vals is not None:
        lower = mean_vals - std_vals
        upper = mean_vals + std_vals

        output = np.hstack([
            x.reshape(-1, 1),
            mean_vals,
            lower,
            upper
        ])

        header = "x mean lower upper"

    else:
        output = np.hstack([
            x.reshape(-1, 1),
            mean_vals
        ])

        header = "x mean_values"

    np.savetxt(OUTPUT, output, header=header)

except Exception as e:
    print(f"[ERROR] Saving failed: {e}")
    sys.exit(1)

# ================================
# PLOT
# ================================

try:

    plt.figure()

    n_curves = mean_vals.shape[1]

    # RDF labels
    if NAME == "rdf_evolution":
        labels = ["0-25%", "25-50%", "50-75%", "75-100%"]
    else:
        labels = [f"curve_{i}" for i in range(n_curves)]

    for i in range(n_curves):

        plt.plot(x, mean_vals[:, i], label=labels[i])

        # ✅ STD only for scalar time series
        if std_vals is not None:
            plt.fill_between(
                x,
                lower[:, i],
                upper[:, i],
                alpha=0.3
            )

    plt.xlabel("x")

    if NAME.startswith("msd"):
        plt.ylabel("MSD")
    elif NAME.startswith("rdf"):
        plt.ylabel("g(r)")
    elif NAME == "coord_Mn":
        plt.ylabel("Coordination")
    elif NAME == "distortion":
        plt.ylabel("Distortion")
    elif NAME == "volume":
        plt.ylabel("Volume")
    else:
        plt.ylabel("Value")

    plt.legend()
    plt.title(NAME)

    plt.savefig(NAME + ".png", dpi=300)
    plt.close()

except Exception as e:
    print(f"[WARNING] Plot failed: {e}")

print("✅ DONE")


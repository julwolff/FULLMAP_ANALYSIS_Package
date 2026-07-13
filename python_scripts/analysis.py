#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 15:12:51 2026

@author: jwjules
"""

import MDAnalysis as mda
import numpy as np
import matplotlib.pyplot as plt
from MDAnalysis.analysis.msd import EinsteinMSD
from MDAnalysis.analysis.rdf import InterRDF
from MDAnalysis.analysis import distances
from pymatgen.core import Lattice, Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from scipy.interpolate import interp1d


# ================================
# PARAMETRES
# ================================

TOPOLOGY = "in.data"
TRAJECTORY = "XX_TRAJECTORY_XX" # Used in the bash script with a sed

TYPE_LI = "type 1"
TYPE_MN = "type 2"
TYPE_O  = "type 3"

TIMESTEP = 0.020  # ps
CUTOFF_MNO = 2.5

# ================================
# LOAD
# ================================

print("Loading trajectory...")

u = mda.Universe(
    TOPOLOGY,
    TRAJECTORY,
    atom_style='id type x y z',
    format="LAMMPSDUMP")

n_frames = len(u.trajectory)
time = np.arange(n_frames) * TIMESTEP


# =============================================================================
#  Sites occupancy
# =============================================================================



def compute_jumps(
        assignment_file="site_assignment.dat"):

    print("Computing jump statistics...")

    data = np.loadtxt(
        assignment_file,
        comments="#",
        dtype=str
    )

    frames  = data[:,0].astype(int)
    atomids = data[:,1].astype(int)
    element = data[:,2]
    sites   = data[:,3].astype(int)

    jumps = []

    jump_matrix = {}

    unique_atoms = np.unique(atomids)

    for atom in unique_atoms:

        mask = atomids == atom

        atom_frames = frames[mask]
        atom_sites  = sites[mask]
        atom_elem   = element[mask][0]

        order = np.argsort(atom_frames)

        atom_frames = atom_frames[order]
        atom_sites  = atom_sites[order]

        for i in range(len(atom_sites)-1):

            s1 = atom_sites[i]
            s2 = atom_sites[i+1]

            if s1 == s2:
                continue

            frame = atom_frames[i+1]

            jumps.append([
                frame,
                atom,
                atom_elem,
                s1,
                s2
            ])

            key = (s1, s2)

            jump_matrix[key] = (
                jump_matrix.get(key, 0) + 1
            )

    with open("jumps.dat", "w") as f:

        f.write(
            "# Frame AtomID Element "
            "FromSite ToSite\n"
        )

        for jump in jumps:

            f.write(
                f"{jump[0]} "
                f"{jump[1]} "
                f"{jump[2]} "
                f"{jump[3]} "
                f"{jump[4]}\n"
            )

    with open("jump_matrix.dat", "w") as f:

        f.write(
            "# FromSite ToSite Count\n"
        )

        for (s1, s2), count in sorted(
                jump_matrix.items()):

            f.write(
                f"{s1} "
                f"{s2} "
                f"{count}\n"
            )

    print(
        f"Detected {len(jumps)} jumps"
    )

    return jumps, jump_matrix


# ==================================
# PARAMETERS
# ==================================

WAVELENGTH = "CuKa"

TWOTHETA_MIN = 10
TWOTHETA_MAX = 90

DUMP_EVERY = 1000
XRD_EVERY  = 200000
XRD_WINDOW = 2000

# atom types
TYPE_MAP = {
    1: "Li",
    2: "Mn",
    3: "O"
}

# ==================================
# XRD
# ==================================

def compute_xrd_series():

    print("Computing XRD series...")

    calculator = XRDCalculator(wavelength=WAVELENGTH)

    total_steps = (len(u.trajectory)-1) * DUMP_EVERY

    centers = np.arange(
        XRD_EVERY,
        total_steps + XRD_EVERY,
        XRD_EVERY
    )

    twotheta_grid = np.linspace(
        TWOTHETA_MIN,
        TWOTHETA_MAX,
        4000
    )

    for center in centers:

        print(f"XRD around step {center}")

        start_step = center - XRD_WINDOW//2
        end_step   = center + XRD_WINDOW//2

        start_frame = max(
            0,
            start_step // DUMP_EVERY
        )

        end_frame = min(
            len(u.trajectory)-1,
            end_step // DUMP_EVERY
        )

        intensity_sum = np.zeros_like(
            twotheta_grid
        )

        nframes = 0

        for iframe in range(
                start_frame,
                end_frame + 1):

            u.trajectory[iframe]

            
            lx, ly, lz, alpha, beta, gamma = u.dimensions


            lattice = Lattice.from_parameters(
                a=lx,
                b=ly,
                c=lz,
                alpha=90,
                beta=90,
                gamma=90
            )

            species = [
                TYPE_MAP[a.type]
                for a in u.atoms
            ]

            coords = u.atoms.positions

            structure = Structure(
                lattice,
                species,
                coords,
                coords_are_cartesian=True
            )

            pattern = calculator.get_pattern(
                structure,
                two_theta_range=(
                    TWOTHETA_MIN,
                    TWOTHETA_MAX
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

        intensity_avg = intensity_sum / nframes

        intensity_avg /= intensity_avg.max()

        np.savetxt(
            f"xrd_{center}.dat",
            np.column_stack(
                (
                    twotheta_grid,
                    intensity_avg
                )
            ),
            header="2theta Intensity"
        )

        print(
            f"Saved xrd_{center}.dat"
        )
        


# Execute

compute_xrd_series()




# ================================
# LARGE DISPLACEMENT DETECTION (Mn ONLY)
# ================================

def detect_large_displacements_Mn(threshold=2.0):

    """
    Detect Mn atoms that significantly moved from their initial position.

    Parameters:
        threshold (float): displacement threshold in Å
    """

    print(f"[INFO] Detecting Mn atoms with displacement > {threshold} Å")

    # sélection Mn
    mn_atoms = u.select_atoms(TYPE_MN)

    # position initiale des Mn
    u.trajectory[0]
    ref_pos = mn_atoms.positions.copy()

    n_atoms = len(mn_atoms)

    max_disp = np.zeros(n_atoms)

    for ts in u.trajectory:

        disp = np.linalg.norm(mn_atoms.positions - ref_pos, axis=1)

        max_disp = np.maximum(max_disp, disp)

    # indices locaux (dans le groupe Mn)
    local_indices = np.where(max_disp > threshold)[0]

    # indices globaux dans le système
    global_indices = mn_atoms.indices[local_indices]

    print(f"[INFO] Found {len(global_indices)} Mn atoms exceeding threshold")

    return global_indices, max_disp, mn_atoms

indices_Mn, max_disp_Mn, mn_atoms = detect_large_displacements_Mn(threshold=3.0)

# ================================
# SAVE Mn DISPLACEMENTS
# ================================

with open("large_displacements_Mn.dat", "w") as f:
    f.write("# index type max_displacement(Angstrom)\n")

    for idx in indices_Mn:
        atom_type = u.atoms[idx].type
        f.write(f"{idx} {atom_type} {max_disp_Mn[mn_atoms.indices.tolist().index(idx)]:.4f}\n")


# ================================
# TRAJECTORY OF MOBILE Mn
# ================================

mobile_Mn = u.atoms[indices_Mn]

with open("mobile_Mn.xyz", "w") as f:

    for ts in u.trajectory:
        f.write(f"{len(mobile_Mn)}\nFrame\n")

        for atom in mobile_Mn:
            x, y, z = atom.position
            f.write(f"{atom.type} {x:.4f} {y:.4f} {z:.4f}\n")
            
# =============================================================================
#  POTENTIAL AND TOTAL ENERGY
# =============================================================================

def extract_energy_from_log(
        logfile="log.lammps",
        step_min=10000,
        step_max=2010000):

    print("Reading energies...")

    steps = []
    pe = []
    te = []

    reading = False
    columns = None

    with open(logfile, "r") as f:

        for line in f:

            words = line.split()

            if not words:
                continue

            if "Step" in words:

                if ("PotEng" in words and
                    ("TotEng" in words or "Etot" in words)):

                    columns = words
                    reading = True

                continue

            if not reading:
                continue

            if words[0] == "Loop":
                reading = False
                continue

            try:

                step = int(float(words[columns.index("Step")]))

                if step < step_min or step > step_max:
                    continue

                PE = float(words[columns.index("PotEng")])

                if "TotEng" in columns:
                    TE = float(words[columns.index("TotEng")])
                else:
                    TE = float(words[columns.index("Etot")])

                steps.append(step)
                pe.append(PE)
                te.append(TE)

            except:
                pass

    np.savetxt(
        "energy.dat",
        np.column_stack((steps, pe, te)),
        header="Step PE TE"
    )

    print("Saved energy.dat")

    return np.array(steps), np.array(pe), np.array(te)

# Execute

steps, PE, TE = extract_energy_from_log(
    logfile="log.lammps",
    step_min=10000,
    step_max=2010000
)


# ================================
# MSD + DIFFUSION
# ================================

def compute_msd_and_diff(selection, label):

    print(f"Computing MSD for {label}...")

    msd = EinsteinMSD(
        u,
        select=selection,
        msd_type='xyz',
    )
    msd.run()

    values = msd.results.timeseries

    # fit zone diffusive
    start = int(0.3 * len(time))
    end   = int(0.8 * len(time))

    slope = np.polyfit(time[start:end], values[start:end], 1)[0]
    D = slope / 6.0

    print(f"{label} diffusion = {D:.3e}")

    return values, D

msd_Li, D_Li = compute_msd_and_diff(TYPE_LI, "Li")
msd_Mn, D_Mn = compute_msd_and_diff(TYPE_MN, "Mn")
msd_O,  D_O  = compute_msd_and_diff(TYPE_O,  "O")

# save MSD
np.savetxt("msd_Li.dat", np.column_stack([time, msd_Li]))
np.savetxt("msd_Mn.dat", np.column_stack([time, msd_Mn]))
np.savetxt("msd_O.dat",  np.column_stack([time, msd_O]))

# diffusion
with open("diffusion.dat", "w") as f:
    f.write("# Species Diffusion\n")
    f.write(f"Li {D_Li}\n")
    f.write(f"Mn {D_Mn}\n")
    f.write(f"O {D_O}\n")

# ================================
# RDF MULTI-COLONNES
# ================================

def compute_rdf_segments(u, sel1, sel2, n_frames,
                         nbins=100, r_range=(0.0, 6.0)):

    print("[INFO] Computing RDF over time segments...")

    # définition des intervalles
    segments = [
        (0, int(0.25 * n_frames)),
        (int(0.25 * n_frames), int(0.50 * n_frames)),
        (int(0.50 * n_frames), int(0.75 * n_frames)),
        (int(0.75 * n_frames), n_frames)
    ]

    labels = ["0_25", "25_50", "50_75", "75_100"]

    rdf_values = []
    r = None

    for (start, stop), label in zip(segments, labels):

        print(f"[INFO] RDF segment {label}: frames {start} → {stop}")

        rdf = InterRDF(
            u.select_atoms(sel1),
            u.select_atoms(sel2),
            nbins=nbins,
            range=r_range
        )

        # ✅ TRUC IMPORTANT
        rdf.run(start=start, stop=stop)

        rdf_values.append(rdf.rdf)

        if r is None:
            r = rdf.bins

    return r, rdf_values, labels


print("Computing RDF evolution...")


# ================================
# RDF MULTI-COLONNES (SEGMENTS)
# ================================

r, rdf_values, labels = compute_rdf_segments(
    u,
    TYPE_MN,
    TYPE_O,
    n_frames
)

# construction matrice
rdf_matrix = np.column_stack([r] + rdf_values)

# sauvegarde
header = "r " + " ".join([f"g_{l}" for l in labels])

np.savetxt(
    "rdf_evolution.dat",
    rdf_matrix,
    header=header
)



# ================================
# COORDINATION
# ================================

def compute_coordination():

    mn = u.select_atoms(TYPE_MN)
    o  = u.select_atoms(TYPE_O)

    values = []

    for ts in u.trajectory:
        d = distances.distance_array(mn.positions, o.positions, box=u.dimensions)
        cn = (d < CUTOFF_MNO).sum(axis=1)
        values.append(np.mean(cn))

    return np.array(values)

coord = compute_coordination()
np.savetxt("coord_Mn.dat", np.column_stack([time, coord]))



# ================================
# DISTORTION
# ================================

def compute_distortion():

    mn = u.select_atoms(TYPE_MN)
    o  = u.select_atoms(TYPE_O)

    values = []

    for ts in u.trajectory:
        d = distances.distance_array(mn.positions, o.positions, box=u.dimensions)

        tmp = []
        for i in range(len(mn)):
            neigh = d[i][d[i] < CUTOFF_MNO]
            if len(neigh) > 1:
                tmp.append(np.std(neigh))

        values.append(np.mean(tmp) if tmp else 0)

    return np.array(values)

dist = compute_distortion()
np.savetxt("distortion.dat", np.column_stack([time, dist]))

# ================================
# VOLUME
# ================================

#vol = []

#for ts in u.trajectory:
#    lx, ly, lz = ts.dimensions[:3]
#    vol.append(lx * ly * lz)

#np.savetxt("volume.dat", np.column_stack([time, vol]))

print("✅ Analysis complete")

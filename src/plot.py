#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob

import numpy as np

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from config.plot_config import *

# ==========================================================
# UTILITIES
# ==========================================================

def save_plot(output_file):

    plt.tight_layout()

    plt.savefig(
        output_file,
        dpi=DPI
    )

    plt.close()

    print(f"[PLOT] {output_file}")


# ==========================================================
# MSD
# ==========================================================

def plot_msd():

    for filename in glob.glob("avg_msd_*.dat"):

        data = np.loadtxt(filename)

        plt.figure(figsize=FIGSIZE)

        plt.plot(
            data[:, 0],
            data[:, 1]
        )

        plt.xlabel("Time (ps)")
        plt.ylabel(r"MSD ($\AA^2$)")

        plt.title(
            filename.replace(".dat", "")
        )

        save_plot(
            filename.replace(".dat", ".png")
        )


# ==========================================================
# RDF
# ==========================================================

def plot_rdf():

    if not glob.glob(
            "avg_rdf_evolution.dat"):
        return

    data = np.loadtxt(
        "avg_rdf_evolution.dat"
    )

    plt.figure(figsize=FIGSIZE)

    for i in range(
            1,
            data.shape[1]):

        plt.plot(
            data[:, 0],
            data[:, i]
        )

    plt.xlabel(r"r ($\AA$)")
    plt.ylabel("g(r)")
    plt.title("Average RDF evolution")

    save_plot(
        "avg_rdf_evolution.png"
    )


# ==========================================================
# COORDINATION
# ==========================================================

def plot_coordination():

    if not glob.glob(
            "avg_coord_Mn.dat"):
        return

    data = np.loadtxt(
        "avg_coord_Mn.dat"
    )

    plt.figure(figsize=FIGSIZE)

    plt.plot(
        data[:, 0],
        data[:, 1]
    )

    plt.xlabel("Time")
    plt.ylabel("Coordination")

    plt.title(
        "Average Mn coordination"
    )

    save_plot(
        "avg_coord_Mn.png"
    )


# ==========================================================
# DISTORTION
# ==========================================================

def plot_distortion():

    if not glob.glob(
            "avg_distortion.dat"):
        return

    data = np.loadtxt(
        "avg_distortion.dat"
    )

    plt.figure(figsize=FIGSIZE)

    plt.plot(
        data[:, 0],
        data[:, 1]
    )

    plt.xlabel("Time")
    plt.ylabel("Distortion")

    plt.title(
        "Average distortion"
    )

    save_plot(
        "avg_distortion.png"
    )


# ==========================================================
# ENERGY
# ==========================================================

def plot_energy():

    if not glob.glob(
            "avg_energy.dat"):
        return

    data = np.loadtxt(
        "avg_energy.dat"
    )

    plt.figure(figsize=FIGSIZE)

    plt.plot(
        data[:, 0],
        data[:, 1],
        label="PE"
    )

    plt.plot(
        data[:, 0],
        data[:, 2],
        label="TE"
    )

    plt.xlabel("Step")
    plt.ylabel("Energy")

    plt.legend()

    save_plot(
        "avg_energy.png"
    )


# ==========================================================
# XRD
# ==========================================================

def plot_xrd():

    for filename in glob.glob(
            "avg_xrd_*.dat"):

        data = np.loadtxt(
            filename
        )

        plt.figure(figsize=FIGSIZE)

        plt.plot(
            data[:, 0],
            data[:, 1]
        )

        plt.xlabel(r"2$\theta$")
        plt.ylabel("Intensity")

        plt.title(
            filename.replace(
                ".dat",
                ""
            )
        )

        save_plot(
            filename.replace(
                ".dat",
                ".png"
            )
        )





# ==========================================================
# RESIDENCE TIMES
# ==========================================================

def plot_residence():

    if not glob.glob(
            "avg_residence_time.dat"):
        return

    data = np.loadtxt(
        "avg_residence_time.dat"
    )

    plt.figure(figsize=FIGSIZE)

    plt.bar(
        data[:, 0],
        data[:, 1]
    )

    plt.xlabel("Site ID")
    plt.ylabel("Residence time (ps)")

    save_plot(
        "avg_residence_time.png"
    )
    

# ==========================================================
# RESIDENCE TIMES
# ==========================================================



def plot_occupancy(
        occupancy_file = "avg_site_occupancy.dat",
        output_file="occupancy.png"):
    """
    Plot antisite occupancies as a function of frame.

    Curves:
    - Li atoms occupying Mn sites
    - Mn atoms occupying Li sites

    Values are plotted as fractions of the
    corresponding atomic population.
    """

    data = np.loadtxt(
        occupancy_file,
        comments="#"
    )

    frames = data[:, 0]

    n_li_li = data[:, 1]
    n_li_mn = data[:, 2]

    n_mn_li = data[:, 3]
    n_mn_mn = data[:, 4]

    # Compute ratios
    li_ratio = (
        n_li_mn /
        (n_li_li + n_li_mn)
    )

    mn_ratio = (
        n_mn_li /
        (n_mn_li + n_mn_mn)
    )

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    ax.plot(
        frames,
        li_ratio,
        lw=2,
        label="Li in Mn sites"
    )

    ax.plot(
        frames,
        mn_ratio,
        lw=2,
        label="Mn in Li sites"
    )

    ax.set_xlabel(
        "Frame"
    )

    ax.set_ylabel(
        "Fraction"
    )

    ax.set_ylim(
        0,
        1
    )

    ax.set_title(
        "Antisite Occupancy"
    )

    ax.legend()

    ax.grid(
        alpha=0.3
    )

    fig.tight_layout()

    plt.savefig(
        output_file,
        dpi=300
    )

    plt.close()

    print(
        f"Occupancy plot written to "
        f"{output_file}"
    )

# ==========================================================
# MASTER FUNCTION
# ==========================================================

def generate_all_plots():

    print("")
    print("======================================")
    print(" GENERATING AVERAGED PLOTS")
    print("======================================")

    if PLOT_MSD:
        plot_msd()

    if PLOT_RDF:
        plot_rdf()

    if PLOT_COORDINATION:
        plot_coordination()

    if PLOT_DISTORTION:
        plot_distortion()

    if PLOT_ENERGY:
        plot_energy()

    if PLOT_XRD:
        plot_xrd()

    if PLOT_OCCUPANCY:
        plot_occupancy()

    if PLOT_RESIDENCE:
        plot_residence()
        
        
    print("")
    print("======================================")
    print(" PLOTS COMPLETE")
    print("======================================")
    
generate_all_plots()
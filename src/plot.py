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
# SITE OCCUPANCY
# ==========================================================

def plot_occupancy():

    if not glob.glob(
            "avg_site_occupancy.dat"):
        return

    data = np.loadtxt(
        "avg_site_occupancy.dat"
    )

    plt.figure(figsize=FIGSIZE)

    plt.bar(
        data[:, 0],
        data[:, 1]
    )

    plt.xlabel("Site ID")
    plt.ylabel("Occupancy")

    save_plot(
        "avg_site_occupancy.png"
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
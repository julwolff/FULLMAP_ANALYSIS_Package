#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RDF analysis module

Produces:
    rdf_evolution.dat

Format:
    r  g_0-1000  g_1000-2000 ...
"""

import numpy as np

from MDAnalysis.analysis.rdf import InterRDF


def compute_rdf_segments(
        u,
        sel1,
        sel2,
        n_segments=10,
        nbins=200,
        r_range=(0.0, 8.0),
        output_file="rdf_evolution.dat"):
    """
    Compute RDF evolution by splitting the trajectory
    into several time segments.

    Parameters
    ----------
    u : MDAnalysis.Universe

    sel1 : str
        First atom selection.

    sel2 : str
        Second atom selection.

    n_segments : int
        Number of trajectory segments.

    nbins : int
        Number of RDF bins.

    r_range : tuple
        RDF range in Å.

    output_file : str
        Output filename.

    Returns
    -------
    r : ndarray
        Distance grid.

    rdf_values : list
        List of RDF arrays.

    labels : list
        Labels associated with each segment.
    """

    print("")
    print("========================================")
    print(" RDF EVOLUTION ANALYSIS")
    print("========================================")

    group1 = u.select_atoms(sel1)
    group2 = u.select_atoms(sel2)

    print(
        f"Selection 1 : {sel1} "
        f"({len(group1)} atoms)"
    )

    print(
        f"Selection 2 : {sel2} "
        f"({len(group2)} atoms)"
    )

    n_frames = len(u.trajectory)

    print(f"Frames       : {n_frames}")
    print(f"Segments     : {n_segments}")
    print(f"Bins         : {nbins}")
    print(f"Range (Å)    : {r_range}")

    segment_size = n_frames // n_segments

    rdf_values = []
    labels = []

    r = None

    for iseg in range(n_segments):

        start = iseg * segment_size

        if iseg == n_segments - 1:
            stop = n_frames
        else:
            stop = (iseg + 1) * segment_size

        print("")
        print(
            f"[SEGMENT {iseg+1}/{n_segments}] "
            f"frames {start} -> {stop}"
        )

        rdf = InterRDF(
            group1,
            group2,
            nbins=nbins,
            range=r_range
        )

        rdf.run(
            start=start,
            stop=stop
        )

        if r is None:
            r = rdf.results.bins

        rdf_values.append(
            rdf.results.rdf.copy()
        )

        labels.append(
            f"{start}-{stop}"
        )

    rdf_matrix = np.column_stack(
        [r] + rdf_values
    )

    header = (
        "r "
        + " ".join(
            [f"g_{label}" for label in labels]
        )
    )

    np.savetxt(
        output_file,
        rdf_matrix,
        header=header
    )

    print("")
    print(f"Saved: {output_file}")
    print("========================================")
    print("")

    return r, rdf_values, labels


def compute_rdf(
        u,
        sel1,
        sel2,
        nbins=200,
        r_range=(0.0, 8.0),
        output_file="rdf.dat"):
    """
    Standard RDF over the whole trajectory.

    Output:
        rdf.dat

    Columns:
        r  g(r)
    """

    print("")
    print("========================================")
    print(" RDF ANALYSIS")
    print("========================================")

    group1 = u.select_atoms(sel1)
    group2 = u.select_atoms(sel2)

    rdf = InterRDF(
        group1,
        group2,
        nbins=nbins,
        range=r_range
    )

    rdf.run()

    r = rdf.results.bins
    g = rdf.results.rdf

    np.savetxt(
        output_file,
        np.column_stack([r, g]),
        header="r g(r)"
    )

    print(f"Saved: {output_file}")

    return r, g

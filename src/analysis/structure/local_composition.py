#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 13:28:46 2026

@author: jwjules
"""

"""
Local composition analysis.

Randomly samples boxes inside the simulation cell and determines
the distribution of local chemical structures.
"""


import numpy as np
from collections import Counter


def count_atoms_in_box(u, center, box_size, type_to_element, debug=False):
    """
    Count atoms inside a local sampling box centered at `center`.

    Parameters
    ----------
    u : MDAnalysis.Universe
        Loaded trajectory.
    center : array-like
        Center of the local box [x, y, z].
    box_size : array-like
        Dimensions of the local box [Lx, Ly, Lz].
    type_to_element : dict
        Mapping from atom type labels to chemical elements.
    debug : bool
        Print debugging information.

    Returns
    -------
    composition : dict
        Number of atoms of each element inside the local box.
    """

    center = np.asarray(center, dtype=float)
    box_size = np.asarray(box_size, dtype=float)

    # ------------------------------------------------------------------
    # Simulation box
    # ------------------------------------------------------------------
    simulation_box = np.asarray(u.dimensions[:3], dtype=float)

    # ------------------------------------------------------------------
    # Atom positions
    # ------------------------------------------------------------------
    positions = u.atoms.positions

    # ------------------------------------------------------------------
    # Minimum-image displacement between every atom and box center
    # ------------------------------------------------------------------
    displacement = positions - center

    displacement -= (
        np.round(displacement / simulation_box)
        * simulation_box
    )

    # ------------------------------------------------------------------
    # Select atoms inside the LOCAL box
    # ------------------------------------------------------------------
    inside = np.all(
        np.abs(displacement) < box_size / 2.0,
        axis=1
    )

    atoms_inside = u.atoms[inside]

    # ------------------------------------------------------------------
    # Count atom types
    # ------------------------------------------------------------------
    composition = {}

    for atom in atoms_inside:

        # MDAnalysis gives atom.type as "1", "2", "3", ...
        # Our package convention is "type 1", "type 2", "type 3"
        atom_type = f"type {atom.type}"

        element = type_to_element.get(atom_type)

        if element is None:
            continue

        composition[element] = (
            composition.get(element, 0) + 1
        )

    # ------------------------------------------------------------------
    # DEBUG
    # ------------------------------------------------------------------
    if debug:

        print("\n" + "=" * 70)
        print("DEBUG : LOCAL BOX")
        print("=" * 70)

        print(f"Center              : {center}")
        print(f"Local box size      : {box_size}")
        print(f"Local box volume    : {np.prod(box_size):.3f} Å³")

        print(f"Simulation box      : {simulation_box}")
        print(
            f"Simulation volume   : "
            f"{np.prod(simulation_box):.3f} Å³"
        )

        print(f"Total atoms         : {len(u.atoms)}")
        print(f"Atoms inside        : {len(atoms_inside)}")

        print("\nComposition:")
        print(composition)

        if len(atoms_inside) > 0:

            print("\nAtoms selected:")

            type_counter = Counter(
                f"type {atom.type}"
                for atom in atoms_inside
            )

            for atom_type, count in sorted(type_counter.items()):
                element = type_to_element.get(
                    atom_type,
                    "UNKNOWN"
                )

                print(
                    f"  {atom_type:8s} "
                    f"({element:2s}) : {count}"
                )

        print("=" * 70)

    return composition


def generate_random_box_center(u, rng):
    """
    Generate a random center for the local box.

    The center is randomly placed inside the simulation box.
    """

    simulation_box = np.asarray(
        u.dimensions[:3],
        dtype=float
    )

    center = rng.uniform(
        low=0.0,
        high=simulation_box
    )

    return center


def structure_formula(composition):
    """
    Convert a composition dictionary into a chemical formula.

    Example
    -------
    {"Li": 1, "Mn": 3, "O": 5}
    -> "Li1Mn3O5"
    """

    # Fixed order for reproducibility
    order = ["Li", "Mn", "O"]

    formula = ""

    for element in order:

        if element in composition:

            formula += (
                f"{element}{composition[element]}"
            )

    return formula


def local_composition_analysis(
    u,
    box_size,
    n_boxes,
    type_to_element,
    output_file,
    seed=None,
    debug=False,
    debug_every=100,
    frame = "first"
):
    """
    Perform random local-composition sampling.

    A small box is randomly positioned inside the simulation
    box `n_boxes` times. The atoms inside each local box are
    counted and converted into a local chemical formula.

    Parameters
    ----------
    u : MDAnalysis.Universe
        Loaded trajectory.

    box_size : float or array-like
        Size of the LOCAL sampling box.

        Example:
            5.0
        gives:
            5 x 5 x 5 Å³

    n_boxes : int
        Number of random local boxes.

    type_to_element : dict
        Mapping between atom types and chemical elements.

    output_file : str
        Output .dat file.

    seed : int, optional
        Random seed.

    debug : bool
        Enable debug output.

    debug_every : int
        Print a summary every N random boxes.
    """
    # ==============================================================
    # SELECT TRAJECTORY FRAME
    # ==============================================================
    
    if frame == "first":
        u.trajectory[0]
    
    elif frame == "last":
        u.trajectory[-1]
    
    else:
        raise ValueError(
            "frame must be either 'first' or 'last'."
        )
    
    if debug:
        print(
            f"\nAnalysing trajectory frame: "
            f"{u.trajectory.frame}"
        )

    # ==============================================================
    # LOCAL BOX SIZE
    # ==============================================================

    if np.isscalar(box_size):

        box_size = np.array(
            [box_size, box_size, box_size],
            dtype=float
        )

    else:

        box_size = np.asarray(
            box_size,
            dtype=float
        )

    if box_size.shape != (3,):

        raise ValueError(
            "box_size must be a scalar "
            "or an array of three values."
        )

    # ==============================================================
    # SIMULATION BOX
    # ==============================================================

    simulation_box = np.asarray(
        u.dimensions[:3],
        dtype=float
    )

    # ==============================================================
    # CHECK LOCAL BOX SIZE
    # ==============================================================

    if np.any(box_size <= 0):

        raise ValueError(
            "Local box dimensions must be positive."
        )

    if np.any(box_size > simulation_box):

        raise ValueError(
            "\nLocal box is larger than the simulation box.\n"
            f"Local box      : {box_size}\n"
            f"Simulation box : {simulation_box}"
        )

    # ==============================================================
    # DEBUG : INITIAL INFORMATION
    # ==============================================================

    if debug:

        print("\n")
        print("#" * 70)
        print("# LOCAL COMPOSITION ANALYSIS")
        print("#" * 70)

        print("\nSimulation:")
        print(
            f"  Box dimensions : "
            f"{simulation_box} Å"
        )

        print(
            f"  Volume         : "
            f"{np.prod(simulation_box):.3f} Å³"
        )

        print(
            f"  Number atoms   : "
            f"{len(u.atoms)}"
        )

        print("\nLocal sampling box:")

        print(
            f"  Dimensions     : "
            f"{box_size} Å"
        )

        print(
            f"  Volume         : "
            f"{np.prod(box_size):.3f} Å³"
        )

        print(
            f"  Number samples : "
            f"{n_boxes}"
        )

        print(
            f"  Random seed    : "
            f"{seed}"
        )

        print("\nAtom type mapping:")

        for atom_type, element in type_to_element.items():

            print(
                f"  {atom_type} -> {element}"
            )

        print("#" * 70)

    # ==============================================================
    # RANDOM NUMBER GENERATOR
    # ==============================================================

    rng = np.random.default_rng(seed)

    # ==============================================================
    # WRAP ATOMS INTO PRIMARY SIMULATION BOX
    # ==============================================================

    u.atoms.wrap()

    # ==============================================================
    # DEBUG : POSITIONS AFTER WRAPPING
    # ==============================================================

    if debug:

        positions = u.atoms.positions

        print("\nAfter wrapping atoms:")

        print(
            f"  Position min : "
            f"{positions.min(axis=0)}"
        )

        print(
            f"  Position max : "
            f"{positions.max(axis=0)}"
        )

        print(
            f"  Simulation box : "
            f"{simulation_box}"
        )

    # ==============================================================
    # RANDOM SAMPLING
    # ==============================================================

    structures = []

    for i in range(n_boxes):

        # ----------------------------------------------------------
        # Random position of the LOCAL box
        # ----------------------------------------------------------

        center = generate_random_box_center(
            u,
            rng
        )

        # ----------------------------------------------------------
        # Count atoms inside local box
        # ----------------------------------------------------------

        composition = count_atoms_in_box(
            u,
            center=center,
            box_size=box_size,
            type_to_element=type_to_element,
            debug=(
                debug
                and (
                    i < 3
                    or i == n_boxes - 1
                )
            ),
        )

        # ----------------------------------------------------------
        # Convert composition into formula
        # ----------------------------------------------------------

        formula = structure_formula(
            composition
        )

        # ----------------------------------------------------------
        # Ignore completely empty boxes
        # ----------------------------------------------------------

        if formula:

            structures.append(formula)

        # ----------------------------------------------------------
        # Progress debug
        # ----------------------------------------------------------

        if debug and (
            (i + 1) % debug_every == 0
        ):

            print(
                f"\nProgress : "
                f"{i + 1}/{n_boxes} boxes"
            )

            print(
                f"Unique structures so far : "
                f"{len(set(structures))}"
            )

    # ==============================================================
    # COUNT STRUCTURES
    # ==============================================================

    counts = Counter(structures)

    # ==============================================================
    # WRITE OUTPUT
    # ==============================================================

    with open(output_file, "w") as f:

        f.write("Structure Count\n")

        for structure, count in counts.items():

            f.write(
                f"{structure} {count}\n"
            )

    # ==============================================================
    # FINAL DEBUG
    # ==============================================================

    if debug:

        print("\n")
        print("#" * 70)
        print("# ANALYSIS COMPLETE")
        print("#" * 70)

        print(
            f"Total random boxes : "
            f"{n_boxes}"
        )

        print(
            f"Non-empty boxes    : "
            f"{len(structures)}"
        )

        print(
            f"Unique structures  : "
            f"{len(counts)}"
        )

        print(
            f"Output file        : "
            f"{output_file}"
        )

        print("\nStructures:")

        for structure, count in counts.most_common():

            print(
                f"  {structure:20s} "
                f"{count}"
            )

        print("#" * 70) 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Build transition matrices between crystallographic SiteTypes.

One transition matrix is generated for each requested atom type.

Rows    = initial SiteType
Columns = final SiteType

M[i,j] = number of transitions i -> j
"""

import numpy as np


def site_transition_matrix(
        file_list,
        output_file,
        atom_types):
    """
    Build one SiteType transition matrix for each requested atom type.

    Parameters
    ----------
    file_list : list of str
        List of site-assignment files.

    output_file : str
        Name of the output file.

    atom_types : list of str
        Atom types to analyse.

        Example:
            ["Li", "Mn"]
    """

    print("=" * 70)
    print("Starting SiteType transition matrix analysis")
    print(
        f"Atom types : "
        f"{', '.join(atom_types)}"
    )
    print(
        f"Number of files to analyse : "
        f"{len(file_list)}"
    )
    print("=" * 70)

    # ==========================================================
    # Storage
    #
    # One set of SiteTypes and transitions for each atom type
    # ==========================================================

    site_types = {
        atom_type: set()
        for atom_type in atom_types
    }

    transitions = {
        atom_type: {}
        for atom_type in atom_types
    }

    # ==========================================================
    # Loop over files
    # ==========================================================

    for file_index, filename in enumerate(
            file_list,
            start=1):

        print("\n" + "-" * 70)
        print(
            f"Processing file "
            f"{file_index}/{len(file_list)}"
        )
        print(f"File : {filename}")

        table = np.loadtxt(
            filename,
            comments="#",
            dtype=str
        )

        frames = np.unique(
            table[:, 0].astype(int)
        )

        print(
            f"Frames detected : "
            f"{len(frames)}"
        )

        # ------------------------------------------------------
        # Store previous SiteType for each atom
        #
        # Key:
        #     AtomID
        #
        # Value:
        #     (AtomType, SiteType)
        # ------------------------------------------------------

        previous_sites = {}

        # ======================================================
        # Loop over frames
        # ======================================================

        for frame_index, frame in enumerate(
                frames,
                start=1):

            if (
                    frame_index == 1
                    or
                    frame_index % 100 == 0
                    or
                    frame_index == len(frames)
            ):

                print(
                    f"   Frame "
                    f"{frame_index}/{len(frames)} "
                    f"(ID = {frame})"
                )

            mask = (
                table[:, 0].astype(int)
                == frame
            )

            data = table[mask]

            # --------------------------------------------------
            # Loop over atoms
            # --------------------------------------------------

            for row in data:

                atom_id = row[1]
                current_atom_type = row[2]

                # Ignore atom types not requested
                if current_atom_type not in atom_types:
                    continue

                # SiteType / crystallographic label
                #
                # Example:
                # 54b
                # 108g
                #
                current_site = row[6]

                # Store SiteType
                site_types[
                    current_atom_type
                ].add(current_site)

                # --------------------------------------------------
                # First occurrence of this atom
                # --------------------------------------------------

                if atom_id not in previous_sites:

                    previous_sites[atom_id] = (
                        current_atom_type,
                        current_site
                    )

                    continue

                previous_atom_type, previous_site = (
                    previous_sites[atom_id]
                )

                # --------------------------------------------------
                # Check transition
                # --------------------------------------------------

                if current_site != previous_site:

                    transition = (
                        previous_site,
                        current_site
                    )

                    if transition not in transitions[
                            current_atom_type]:

                        transitions[
                            current_atom_type
                        ][transition] = 0

                    transitions[
                        current_atom_type
                    ][transition] += 1

                # --------------------------------------------------
                # Update previous SiteType
                # --------------------------------------------------

                previous_sites[atom_id] = (
                    current_atom_type,
                    current_site
                )

        print("File completed.")

    # ==========================================================
    # Write output
    # ==========================================================

    print("\n" + "=" * 70)
    print("Writing transition matrices...")
    print(
        f"Output file : "
        f"{output_file}"
    )

    with open(
            output_file,
            "w") as f:

        # ------------------------------------------------------
        # One matrix per atom type
        # ------------------------------------------------------

        for atom_type in atom_types:

            sorted_sites = sorted(
                site_types[atom_type]
            )

            n_sites = len(sorted_sites)

            print("")
            print(
                f"{atom_type} transition matrix"
            )
            print(
                f"Number of SiteTypes : "
                f"{n_sites}"
            )

            # --------------------------------------------------
            # Build matrix
            # --------------------------------------------------

            matrix = np.zeros(
                (n_sites, n_sites),
                dtype=int
            )

            site_index = {
                site: i
                for i, site in enumerate(
                    sorted_sites
                )
            }

            # --------------------------------------------------
            # Fill matrix
            # --------------------------------------------------

            for (
                    initial_site,
                    final_site
            ), count in transitions[
                    atom_type].items():

                i = site_index[
                    initial_site
                ]

                j = site_index[
                    final_site
                ]

                matrix[i, j] = count

            # --------------------------------------------------
            # Write matrix header
            # --------------------------------------------------

            f.write(
                f"# ==================================================\n"
            )

            f.write(
                f"# Atom type: {atom_type}\n"
            )

            f.write(
                f"# Rows    : Initial SiteType\n"
            )

            f.write(
                f"# Columns : Final SiteType\n"
            )

            f.write(
                f"# ==================================================\n"
            )

            f.write(
                "# InitialSite "
                +
                " ".join(sorted_sites)
                +
                "\n"
            )

            # --------------------------------------------------
            # Write matrix
            # --------------------------------------------------

            for i, site in enumerate(
                    sorted_sites):

                f.write(
                    f"{site} "
                )

                f.write(
                    " ".join(
                        str(value)
                        for value in matrix[i]
                    )
                )

                f.write("\n")

            f.write("\n")

    print(
        f"Transition matrices saved to "
        f"{output_file}"
    )

    print("=" * 70)
    print(
        "SiteType transition matrix "
        "analysis completed."
    )
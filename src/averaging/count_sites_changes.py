#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 13:27:04 2026

@author: jwjules
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Count transitions between crystallographic SiteTypes.

Example:

    54b -> 108g

is counted whenever an atom changes from SiteType 54b
to SiteType 108g between two consecutive frames.
"""

import numpy as np


def count_site_type_changes(
        file_list,
        output_file):
    """
    Count changes between crystallographic SiteTypes.

    Parameters
    ----------
    file_list : list of str
        List of site-assignment files.

    output_file : str
        Name of the output file.
    """

    print("=" * 70)
    print("Starting SiteType transition analysis")
    print(f"Number of files to analyse : {len(file_list)}")
    print("=" * 70)

    # ==========================================================
    # Dictionary storing transitions
    #
    # Key:
    #     (AtomType, InitialSiteType, FinalSiteType)
    #
    # Value:
    #     Number of transitions
    # ==========================================================

    transitions = {}

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

        print(f"Rows loaded : {len(table)}")

        frames = np.unique(
            table[:, 0].astype(int)
        )

        print(f"Frames detected : {len(frames)}")

        # ------------------------------------------------------
        # Previous SiteType for every atom
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
                atom_type = row[2]

                # SiteType / crystallographic label
                #
                # Example:
                # 54b
                # 108g
                #
                current_site = row[6]

                # First frame for this atom
                if atom_id not in previous_sites:

                    previous_sites[atom_id] = (
                        atom_type,
                        current_site
                    )

                    continue

                previous_atom_type, previous_site = (
                    previous_sites[atom_id]
                )

                # --------------------------------------------------
                # Detect transition
                # --------------------------------------------------

                if current_site != previous_site:

                    transition = (
                        atom_type,
                        previous_site,
                        current_site
                    )

                    if transition not in transitions:

                        transitions[transition] = 0

                    transitions[transition] += 1

                # Update previous SiteType
                previous_sites[atom_id] = (
                    atom_type,
                    current_site
                )

        print("File completed.")

    # ==========================================================
    # Write output
    # ==========================================================

    print("\n" + "=" * 70)
    print("Writing output file...")
    print(f"Output file : {output_file}")

    with open(
            output_file,
            "w") as f:

        f.write(
            "# AtomType "
            "InitialSiteType "
            "FinalSiteType "
            "NumberOfChanges\n"
        )

        for transition in sorted(
                transitions.keys()):

            atom_type = transition[0]
            initial_site = transition[1]
            final_site = transition[2]

            count = transitions[transition]

            f.write(
                f"{atom_type} "
                f"{initial_site} "
                f"{final_site} "
                f"{count}\n"
            )

    print("Output successfully written.")
    print("=" * 70)
    print("SiteType transition analysis completed.")
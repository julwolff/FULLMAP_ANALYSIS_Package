#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 15:55:12 2026

@author: jwjules
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Aug 6 15:55:12 2026

@author: jwjules
"""

import numpy as np


def average_site_occupancy(
        file_list,
        output_file):
    """
    Compute the total site occupancy for each simulation frame.

    For every input file, the function counts the number of atoms
    occupying each type of crystallographic site. Four combinations
    are considered:

        - Li atom located in a Li site
        - Li atom located in a Mn site
        - Mn atom located in a Li site
        - Mn atom located in a Mn site

    The occupancies are accumulated frame by frame over all input
    files before being written to the output file.

    Parameters
    ----------
    file_list : list of str
        List of input files.

    output_file : str
        Name of the output file.
    """

    print("=" * 70)
    print("Starting site occupancy analysis")
    print(f"Number of files to analyse : {len(file_list)}")
    print("=" * 70)

    # Dictionary storing cumulative occupancies
    # Key   : frame number
    # Value : [Li@Li, Li@Mn, Mn@Li, Mn@Mn]
    occupancy = {}

    # ==========================================================
    # Loop over all files
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

        # ------------------------------------------------------
        # Load file
        # ------------------------------------------------------

        table = np.loadtxt(
            filename,
            comments="#",
            dtype=str
        )

        print(f"Rows loaded : {len(table)}")

        # ------------------------------------------------------
        # Extract all frame numbers
        # ------------------------------------------------------

        frames = np.unique(
            table[:, 0].astype(int)
        )

        print(f"Frames detected : {len(frames)}")
        print(
            f"Frame range : "
            f"{frames[0]} -> {frames[-1]}"
        )

        # ======================================================
        # Loop over frames
        # ======================================================

        for frame_index, frame in enumerate(
                frames,
                start=1):

            # Print progress every 100 frames
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

            # Counters
            n_li_li = 0
            n_li_mn = 0
            n_mn_li = 0
            n_mn_mn = 0

            # --------------------------------------------------
            # Loop over atoms
            # --------------------------------------------------

            for row in data:

                atom_type = row[2]
                site_type = row[4]

                if (
                        atom_type == "Li"
                        and
                        site_type == "Li"
                ):

                    n_li_li += 1

                elif (
                        atom_type == "Li"
                        and
                        site_type == "Mn"
                ):

                    n_li_mn += 1

                elif (
                        atom_type == "Mn"
                        and
                        site_type == "Li"
                ):

                    n_mn_li += 1

                elif (
                        atom_type == "Mn"
                        and
                        site_type == "Mn"
                ):

                    n_mn_mn += 1

            # --------------------------------------------------
            # Initialize frame if necessary
            # --------------------------------------------------

            if frame not in occupancy:

                occupancy[frame] = np.zeros(
                    4,
                    dtype=int
                )

            # --------------------------------------------------
            # Add counts to cumulative occupancy
            # --------------------------------------------------

            occupancy[frame] += np.array(
                [
                    n_li_li,
                    n_li_mn,
                    n_mn_li,
                    n_mn_mn
                ]
            )

        print("File completed.")

    # ==========================================================
    # Write output
    # ==========================================================

    print("\n" + "=" * 70)
    print("Writing output file...")
    print(f"Output file : {output_file}")
    print(f"Frames to write : {len(occupancy)}")

    with open(
            output_file,
            "w") as f:

        f.write(
            "# Frame "
            "NLiatomsinLiSites "
            "NLiatomsinMnSites "
            "NMnatomsinLiSites "
            "NMnatomsinMnSites\n"
        )

        for frame in sorted(
                occupancy.keys()):

            values = occupancy[frame]

            f.write(
                f"{frame} "
                f"{values[0]} "
                f"{values[1]} "
                f"{values[2]} "
                f"{values[3]}\n"
            )

    print("Output successfully written.")
    print("=" * 70)
    print("Site occupancy analysis completed successfully.")
    print("=" * 70)
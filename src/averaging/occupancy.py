import numpy as np


def average_site_occupancy(file_list, output_file):

    occupancy = {}

    print("=" * 70)
    print("SITE OCCUPANCY ANALYSIS")
    print(f"Number of files : {len(file_list)}")
    print("=" * 70)

    for file_index, filename in enumerate(file_list, start=1):

        print()
        print(f"[{file_index}/{len(file_list)}] Processing: {filename}")

        # ------------------------------------------------------
        # Load file
        # ------------------------------------------------------

        data = np.loadtxt(
            filename,
            comments="#",
            dtype=str,
            ndmin=2
        )

        frames = data[:, 0].astype(int)
        atom_type = data[:, 2]
        site_atom_type = data[:, 4]

        unique_frames = np.unique(frames)
        n_frames = len(unique_frames)

        print(f"    Frames: {n_frames}")

        # ------------------------------------------------------
        # Analyse frames
        # ------------------------------------------------------

        for frame_index, frame in enumerate(
            unique_frames,
            start=1
        ):

            mask = frames == frame

            atoms = atom_type[mask]
            sites = site_atom_type[mask]

            # --------------------------------------------------
            # Count occupations
            # --------------------------------------------------

            Li_in_Li = np.sum(
                (atoms == "Li") & (sites == "Li")
            )

            Li_in_Mn = np.sum(
                (atoms == "Li") & (sites == "Mn")
            )

            Mn_in_Li = np.sum(
                (atoms == "Mn") & (sites == "Li")
            )

            Mn_in_Mn = np.sum(
                (atoms == "Mn") & (sites == "Mn")
            )

            values = np.array([
                Li_in_Li,
                Li_in_Mn,
                Mn_in_Li,
                Mn_in_Mn
            ])

            # --------------------------------------------------
            # Add to cumulative result
            # --------------------------------------------------

            if frame not in occupancy:
                occupancy[frame] = values
            else:
                occupancy[frame] += values

            # --------------------------------------------------
            # Progress
            # --------------------------------------------------

            percent = 100 * frame_index / n_frames

            print(
                f"\r    Frame {frame_index}/{n_frames} "
                f"({percent:6.2f}%)",
                end="",
                flush=True
            )

        print()  # New line after progress

    # ==========================================================
    # Write output
    # ==========================================================

    print()
    print("=" * 70)
    print("Writing output")
    print("=" * 70)

    with open(output_file, "w") as f:

        f.write(
            "# Frame "
            "NLiatomsinLiSites "
            "NLiatomsinMnSites "
            "NMnatomsinLiSites "
            "NMnatomsinMnSites\n"
        )

        for frame in sorted(occupancy):

            values = occupancy[frame]

            f.write(
                f"{frame} "
                f"{values[0]} "
                f"{values[1]} "
                f"{values[2]} "
                f"{values[3]}\n"
            )

    print(f"Output written to: {output_file}")
    print("=" * 70)
    print("Analysis completed.")
    print("=" * 70)
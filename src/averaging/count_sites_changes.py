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


import numpy as np
from collections import Counter


def count_site_type_changes(file_list, output_file):

    transitions = Counter()

    print("=" * 60)
    print("SiteType transition analysis")
    print(f"Files to analyse : {len(file_list)}")
    print("=" * 60)

    for file_index, filename in enumerate(file_list, start=1):

        print(f"\n[{file_index}/{len(file_list)}] Processing: {filename}")

        data = np.loadtxt(
            filename,
            dtype=str,
            comments="#"
        )

        print(f"    Rows loaded: {len(data)}")

        previous_sites = {}

        frames = data[:, 0].astype(int)
        n_frames = len(np.unique(frames))
        current_frame = None
        frame_index = 0

        for row in data:

            frame = int(row[0])

            # Progression when entering a new frame
            if frame != current_frame:

                current_frame = frame
                frame_index += 1

                if (
                    frame_index == 1
                    or frame_index % 100 == 0
                    or frame_index == n_frames
                ):
                    print(
                        f"    Frame {frame_index}/{n_frames} "
                        f"(ID = {frame})"
                    )

            atom_id = row[1]
            atom_type = row[2]
            current_site = row[6]

            if atom_id in previous_sites:

                previous_site = previous_sites[atom_id]

                if current_site != previous_site:

                    transitions[
                        (atom_type, previous_site, current_site)
                    ] += 1

            previous_sites[atom_id] = current_site

        print("    File completed.")

    print("\n" + "=" * 60)
    print("Writing results")
    print(f"Output file: {output_file}")

    with open(output_file, "w") as f:

        for (atom_type, initial_site, final_site), count in sorted(
            transitions.items()
        ):
            f.write(
                f"{atom_type} "
                f"{initial_site} "
                f"{final_site} "
                f"{count}\n"
            )

    print(f"Transitions found: {len(transitions)}")
    print("Analysis completed.")
    print("=" * 60)
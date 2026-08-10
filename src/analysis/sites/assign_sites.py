#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from MDAnalysis.lib.distances import distance_array

def assign_sites(
        atom_position,
        site_positions):
    """
    Return the index of the closest site.
    """

    distances = np.linalg.norm(
        site_positions - atom_position,
        axis=1
    )

    return np.argmin(distances)


def assign_sites_trajectory(
        u,
        sites_file="sites.dat",
        output_file="site_assignment.dat"):
    """
    Assign Li and Mn atoms to the nearest crystallographic sites
    for every frame of a trajectory.
    """

    # ==========================================================
    # Initialize analysis
    # ==========================================================
    print("")
    print("========================================")
    print(" SITE ASSIGNMENT")
    print("========================================")

    # ==========================================================
    # Load site information
    # ==========================================================
    print(f"Reading site file: {sites_file}")

    sites = np.loadtxt(
        sites_file,
        comments="#",
        dtype=str
    )

    # Extract site metadata
    site_ids = sites[:, 0].astype(int)
    elements = sites[:, 1]
    coords = sites[:, 3:6].astype(float)

    # Compute basic statistics about available sites
    n_sites = len(site_ids)
    n_li_sites = np.sum(elements == "Li")
    n_mn_sites = np.sum(elements == "Mn")

    # ==========================================================
    # Report loaded site information
    # ==========================================================
    print("")
    print("Loaded site information:")
    print(f"  Total sites : {n_sites}")
    print(f"  Li sites    : {n_li_sites}")
    print(f"  Mn sites    : {n_mn_sites}")

    # Determine the number of trajectory frames
    n_frames = len(u.trajectory)

    print("")
    print(f"Trajectory contains {n_frames} frames")

    assignment_count = 0

    # ==========================================================
    # Open output file and process trajectory
    # ==========================================================
    with open(output_file, "w") as f:

        # Write output header
        f.write(
            "# Frame AtomID AtomType SiteID SiteType Distance\n"
        )

        # Loop over trajectory frames
        for iframe, ts in enumerate(u.trajectory):
            
            u.atoms.wrap()

            # Progress update every 100 frames
            if (
                iframe % 100 == 0
                or
                iframe == n_frames - 1
            ):
                print(
                    f"Processing frame "
                    f"{iframe + 1}/{n_frames}"
                )

            frame_assignments = 0

            # --------------------------------------------------
            # Loop over all atoms in current frame
            # --------------------------------------------------
            for atom in u.atoms:

                # Convert atom type to chemical symbol
                symbol = {
                    1: "Li",
                    2: "Mn",
                    3: "O"
                }.get(int(atom.type))

                # Only Li and Mn atoms are assigned
                if symbol not in ["Li", "Mn"]:
                    continue

                # Search among all available sites
                # Search among all available sites
                distances = distance_array(
                    atom.position.reshape(1, 3),
                    coords,
                    box=ts.dimensions
                )[0]
                
                # Find closest site
                imin = np.argmin(distances)
                
                dmin = distances[imin]
                
                closest_site = site_ids[imin]
                closest_site_element = elements[imin]
                
                closest_site_coord = coords[imin]
                
                # # ======================================================
                # # DEBUG
                # # ======================================================
                # print("\n[DEBUG]")
                
                # print(
                #     f"Frame      : {iframe}"
                # )
                
                # print(
                #     f"Atom ID    : {atom.id}"
                # )
                
                # print(
                #     f"Atom type  : {symbol}"
                # )
                
                # print(
                #     f"Atom coord : {atom.position}"
                # )
                
                # print(
                #     f"Site ID    : {closest_site}"
                # )
                
                # print(
                #     f"Site type  : {closest_site_element}"
                # )
                
                # print(
                #     f"Site coord : {closest_site_coord}"
                # )
                
                # print(
                #     f"Delta      : "
                #     f"{atom.position - closest_site_coord}"
                # )
                
                # print(
                #     f"Distance   : {dmin:.4f} Å"
                # )
                


                
                # Threshold check
                if dmin > 1e9:
                
  
                    site = "TH"
                
                else:
                
                    site = closest_site

                
                    


                # Save assignment
                f.write(
                    f"{iframe} "
                    f"{atom.id} "
                    f"{symbol} "
                    f"{site} "
                    f"{closest_site_element} "
                    f"{dmin:.6f}\n"
                )
                
                frame_assignments += 1
                assignment_count += 1

            # Report frame statistics
            if (
                iframe % 100 == 0
                or
                iframe == n_frames - 1
            ):
                print(
                    f"  Assigned "
                    f"{frame_assignments} atoms"
                )

    # ==========================================================
    # Final summary
    # ==========================================================
    print("")
    print("Assignment completed")

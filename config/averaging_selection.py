#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analysis selection.

False  -> run analysis
False -> skip analysis
"""

AVERAGING = {

    "msd_Li": True,
    "msd_Mn": True,
    "msd_O": True,

    "rdf_evolution": True,
    
    "coord_Mn": True,

    "distortion": True,

    "energy": True,

    "diffusion": True,

    "site_occupancy": False,

    "jump_matrix": False,

    "residence_time": False,

    "xrd": True
}

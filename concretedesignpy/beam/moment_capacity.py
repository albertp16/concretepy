#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# MIT License
# 
# Author: Albert Pamonag
# Year: 2023
#
# Description:
#   This script processes rebar data using a vectorized NumPy approach to compute 
#   the cross-sectional area for each rebar entry.

import math
import numpy as np

def process_rebar_data(rebar_list):
    """
    Fast, vectorized approach to process a list of rebar dictionaries and compute
    each rebar's cross-sectional area.
    
    Parameters
    ----------
    rebar_list : list of dict
        A list of dictionaries, where each dictionary must have the following keys:
            - "d"    (float): The distance of the rebar from a reference point (e.g., cover).
            - "diam" (float): The diameter of the rebar in mm or inches (depending on units).
            - "num"  (int)  : The number of rebars of that diameter and location.
        Example:
            [
                {"d": 58,  "diam": 16, "num": 2},
                {"d": 342, "diam": 16, "num": 3},
                ...
            ]
    
    Returns
    -------
    result : dict
        A dictionary containing:
        
        "value" : list of dict
            A list of dictionaries with the same fields as input plus an additional key:
                - "as" (float): The computed cross-sectional area of the rebars.
            
        "report" : str
            A human-readable multi-line string summarizing the computed values for each entry.
    """
    # 1) Extract columns from the list of dicts into NumPy arrays
    ds    = np.array([r["d"]    for r in rebar_list], dtype=float)
    diams = np.array([r["diam"] for r in rebar_list], dtype=float)
    nums  = np.array([r["num"]  for r in rebar_list],  dtype=int)

    # 2) Compute areas in one vector operation
    #    area_i = π * (diam_i / 2)^2 * num_i
    areas = math.pi * (diams / 2.0)**2 * nums

    # 3) Build output list of dict and the report
    processed = []
    lines = ["rebar data (d, diam, num, as):"]

    for i in range(len(rebar_list)):
        item = {
            "d": ds[i],
            "diam": diams[i],
            "num": nums[i],
            "as": areas[i]
        }
        processed.append(item)
        lines.append(
            f"  d={ds[i]:7.2f}, "
            f"diam={diams[i]:5.2f}, "
            f"num={nums[i]:2d}, "
            f"as={areas[i]:10.2f}"
        )

    return {
        "value": processed,
        "report": "\n".join(lines)
    }

rebars = [
        {'d': 58,  'diam': 16, 'num': 2},  # top (compression) bars
        {'d': 342, 'diam': 16, 'num': 3},  # bottom (tension) bars
]



# print(process_rebar_data(rebars)['value'])

def calculate_rebar_forces(
    rebar_list, beam_height, beam_width,
    fc, fy, es, ecu, steel_strain, beta_one
):
    
    dt = beam_height
    current_x = dt
    iter_num = 50
    iter_step = dt / iter_num
    update_step = True
    alpha_2 = 0.85

    x_output = None
    solution_found = False

    iteration_data = []
    i = 0
    pass_count = 1

    # final forces
    fcc_final = 0.0
    fcsi_final = 0.0
    fsi_final = 0.0
    ratio_final = None

    while i < iter_num:
        if i == 0:
            x = current_x
        else:
            x = current_x - iter_step
            current_x = x

        # compute compression & tension rebar
        fcsi_rebar = 0.0
        fsi_rebar = 0.0
        for bar in rebar_list:
            d_i = bar["d"]
            as_i = bar["as"]
            if d_i < x:
                # compression zone
                esci = ((x - d_i)/x)*ecu
                f_sci = min(esci*es, fy)
                fi = as_i*f_sci
                fcsi_rebar += fi
            else:
                # tension zone
                esti = ((d_i - x)/x)*ecu
                f_sti = min(esti*es, fy)
                fi = as_i*f_sti
                fsi_rebar += fi

        # concrete block
        a_comp = beta_one * x * beam_width
        f_concrete = alpha_2 * fc * a_comp
        fci = f_concrete + fcsi_rebar
        fsi = fsi_rebar
        ratio = fci/fsi if fsi != 0 else float('inf')

        iteration_data.append({
            "pass": pass_count,
            "iteration": i+1,
            "x": x,
            "fc_concrete_kN": f_concrete/1000.0,
            "fc_rebar_kN": fcsi_rebar/1000.0,
            "fs_rebar_kN": fsi_rebar/1000.0,
            "fci_kN": (f_concrete + fcsi_rebar)/1000.0,
            "ratio": ratio
        })

        if not update_step:
            if fci <= fsi:
                x_output = x
                fcc_final = f_concrete
                fcsi_final = fcsi_rebar
                fsi_final = fsi_rebar
                ratio_final = ratio
                solution_found = True
                break
        else:
            if fci <= fsi:
                update_step = False
                # store final
                x_output = x
                fcc_final = f_concrete
                fcsi_final = fcsi_rebar
                fsi_final = fsi_rebar
                ratio_final = ratio
                solution_found = True

                # revert x by adding step
                current_x += iter_step
                # refine step
                iter_step = iter_step / iter_num
                pass_count += 1
                i = -1  # so next loop iteration will be i=0
        i += 1

    return {
        "iteration_data": iteration_data,
        "neutral_axis": x_output,
        "fc_concrete": fcc_final,
        "fc_rebar": fcsi_final,
        "fs_rebar": fsi_final,
        "ratio": ratio_final
    }

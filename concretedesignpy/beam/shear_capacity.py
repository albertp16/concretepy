#!/usr/bin/env python3
"""
Module: shear.py

This module provides functions to validate design parameters for transverse
reinforcements according to Section 418.6.4. It includes validations for the
first hoop location, maximum allowable hoop spacing, and conditions where hoops
are not required.
"""

import math

def validate_first_hoop(first_hoop_loc: float) -> bool:
    """
    Validates the location of the first hoop relative to the face of the supporting member.

    Parameters:
        first_hoop_loc (float): Distance (in mm) from the face to the first hoop.

    Returns:
        bool: True if the first hoop is within 50 mm, False otherwise.
    """
    if first_hoop_loc > 50:
        print("Warning: The first hoop should be within 50 mm of the face of the supporting member.")
        return False
    return True

def validate_max_hoop_spacing(depth: float, db: float, ds: float, hoop_spacing: float) -> bool:
    """
    Validates that the provided hoop spacing does not exceed the maximum allowed value.

    The maximum allowed spacing is defined as the minimum of:
        - depth / 4,
        - 6 * db,
        - 24 * ds,
        - 150 (mm)

    Parameters:
        depth (float): Effective depth of the member (mm).
        db (float): Diameter of the bar (mm).
        ds (float): Diameter of the stirrup (mm).
        hoop_spacing (float): Provided spacing between hoops (mm).

    Returns:
        bool: True if the hoop spacing is within the allowed limit, False otherwise.
    """
    max_spacing = min(depth / 4, 6 * db, 24 * ds, 150)
    if hoop_spacing > max_spacing:
        print(f"Warning: Provided hoop spacing ({hoop_spacing:.2f} mm) exceeds the limit of {max_spacing:.2f} mm.")
        return False
    return True

def validate_hoops_not_required(depth: float, hoop_spacing: float) -> bool:
    """
    Validates the hoop spacing for cases where hoops are not required (per Section 418.6.4.6).

    The maximum allowed spacing in this case is:
        - depth / 2

    Parameters:
        depth (float): Effective depth of the member (mm).
        hoop_spacing (float): Provided spacing between hoops (mm).

    Returns:
        bool: True if the spacing is within the allowed limit, False otherwise.
    """
    max_spacing = depth / 2
    if hoop_spacing > max_spacing:
        print(f"Warning: Provided hoop spacing ({hoop_spacing:.2f} mm) exceeds the limit of {max_spacing:.2f} mm.")
        return False
    return True

def validate_max_spacing(db: float, hoop_spacing: float) -> bool:
    """
    Validates the maximum hoop spacing based on the bar diameter.

    The maximum allowed spacing is the minimum of:
        - 6 * db,
        - 150 (mm)

    Parameters:
        db (float): Diameter of the bar (mm).
        hoop_spacing (float): Provided spacing between hoops (mm).

    Returns:
        bool: True if the hoop spacing is within the allowed limit, False otherwise.
    """
    max_spacing = min(6 * db, 150)
    if hoop_spacing > max_spacing:
        print(f"Warning: Provided hoop spacing ({hoop_spacing:.2f} mm) exceeds the limit of {max_spacing:.2f} mm.")
        return False
    return True


def calculate_vc(fc,beam_width,eff_depth):
    '''
    fc = in MPa
    beam_with = in mm
    eff_depth = in mm
    '''
    CONSTANT = 1/6
    value = CONSTANT*math.sqrt(fc)*beam_width*eff_depth
    return value 

def calculate_vs(av,fy,eff_depth,spacing):
    '''
    av = area of steel reinforcement (shear)
    fy = yeild strength 
    s = spacing of shear reinforcement 
    d = effective depth
    '''
    value = (av*fy*eff_depth)/spacing
    return value


def main():
    """
    Demonstrates example validations for transverse reinforcements.
    """
    # Example parameters (in mm)
    first_hoop_loc = 55   # Distance of the first hoop from the face
    depth = 200           # Effective depth of the member
    db = 16               # Bar diameter
    ds = 8                # Stirrup diameter
    hoop_spacing = 60     # Provided hoop spacing

    # Validate first hoop location
    if not validate_first_hoop(first_hoop_loc):
        print("First hoop location validation failed.")

    # Validate maximum hoop spacing
    if not validate_max_hoop_spacing(depth, db, ds, hoop_spacing):
        print("Maximum hoop spacing validation failed.")

    # Validate hoops not required scenario
    if not validate_hoops_not_required(depth, hoop_spacing):
        print("Hoops not required spacing validation failed.")

    # Validate maximum spacing based on bar diameter
    if not validate_max_spacing(db, hoop_spacing):
        print("Maximum spacing based on bar diameter validation failed.")

if __name__ == "__main__":
    main()

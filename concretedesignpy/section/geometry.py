import matplotlib.pyplot as plt

# =============================================================================
# Function: compute_rebar_coordinates
# =============================================================================
def compute_rebar_coordinates(width, height, cover, ds, db, nx, ny):
    """
    Compute the coordinates for the rebar layout in a beam cross-section.

    Parameters:
        width    : Section width  [mm]
        height   : Section height [mm]
        cover    : Concrete cover (to stirrup outer face) [mm]
        ds       : Diameter of stirrups   [mm]
        db       : Diameter of main bars  [mm]
        nx       : Number of bars along top & bottom
        ny       : Number of bars along left & right

    Returns:
        dict: {
            'section_corners': 4 points (x, y) for the OUTER rectangle (unconfined section),
            'stirrup_corners': 4 points (x, y) for the STIRRUP CENTER-LINE rectangle,
            'rebar_coords':    (x, y) locations for each main rebar
        }
    """
    # --- 1) Outer rectangle corners (unconfined section) ---
    section_corners = [
        (0.0,  0.0),       # bottom-left
        (width,  0.0),     # bottom-right
        (width,  height),  # top-right
        (0.0,  height)     # top-left
    ]

    # --- 2) Stirrup center-line corners (confined section) ---
    # Offset from the outer face by (cover + 0.5 * ds)
    stirrup_offset = cover + 0.5 * ds
    stirrup_corners = [
        (stirrup_offset,             stirrup_offset),
        (width - stirrup_offset,     stirrup_offset),
        (width - stirrup_offset,     height - stirrup_offset),
        (stirrup_offset,             height - stirrup_offset)
    ]

    # --- 3) Main bar offset from the outer face ---
    # = cover + ds + 0.5 * db
    rebar_offset = cover + ds + 0.5 * db
    x_left  = rebar_offset
    x_right = width - rebar_offset
    y_bot   = rebar_offset
    y_top   = height - rebar_offset

    # --- 4) Compute rebar coordinates ---
    rebar_coords = []

    # Horizontal bars (top & bottom)
    if nx == 1:
        x_positions = [(x_left + x_right) / 2.0]
    else:
        dx = (x_right - x_left) / (nx - 1)
        x_positions = [x_left + i * dx for i in range(nx)]
    for x_pos in x_positions:
        rebar_coords.append((x_pos, y_bot))  # bottom bar
        rebar_coords.append((x_pos, y_top))  # top bar

    # Vertical bars (left & right)
    if ny == 1:
        y_positions = [(y_bot + y_top) / 2.0]
    else:
        dy = (y_top - y_bot) / (ny - 1)
        y_positions = [y_bot + i * dy for i in range(ny)]
    for y_pos in y_positions:
        rebar_coords.append((x_left,  y_pos))  # left bar
        rebar_coords.append((x_right, y_pos))  # right bar

    # Remove duplicates (corner bars appear in both sets)
    rebar_coords = list(set(rebar_coords))
    rebar_coords.sort(key=lambda pt: (pt[1], pt[0]))

    return {
        "section_corners": section_corners,
        "stirrup_corners": stirrup_corners,
        "rebar_coords": rebar_coords
    }


# =============================================================================
# Function: plot_beam_rebar
# =============================================================================
def plot_beam_rebar(width, height, section_corners, stirrup_corners, rebar_coords, show_labels=True):
    """
    Plot the beam cross-section with the rebar layout.

    Parameters:
        width           : Section width [mm]
        height          : Section height [mm]
        section_corners : List of 4 points for the outer rectangle (unconfined section)
        stirrup_corners : List of 4 points for the stirrup center-line rectangle (confined section)
        rebar_coords    : List of (x, y) coordinates for each main rebar
        show_labels     : If True, labels are added to the plot
    """
    fig, ax = plt.subplots(figsize=(5, 6))

    # --- 1) Plot the outer rectangle (unconfined section) ---
    x_vals = [p[0] for p in section_corners] + [section_corners[0][0]]
    y_vals = [p[1] for p in section_corners] + [section_corners[0][1]]
    ax.plot(x_vals, y_vals, 'k-', linewidth=2, label="Unconfined Section")

    # --- 2) Plot the stirrup center-line rectangle ---
    sx_vals = [p[0] for p in stirrup_corners] + [stirrup_corners[0][0]]
    sy_vals = [p[1] for p in stirrup_corners] + [stirrup_corners[0][1]]
    ax.plot(sx_vals, sy_vals, 'b--', linewidth=1.5, label="Stirrup (Center-Line)")

    # --- 3) Plot the rebar points ---
    rx = [p[0] for p in rebar_coords]
    ry = [p[1] for p in rebar_coords]
    ax.scatter(rx, ry, s=60, c='red', marker='o', label="Main Bars")

    # --- 4) Add labels if required ---
    if show_labels:
        for i, pt in enumerate(section_corners, start=1):
            ax.text(pt[0], pt[1], f"C{i}", color='blue', fontsize=9, ha='left', va='bottom')
        for i, pt in enumerate(stirrup_corners, start=1):
            ax.text(pt[0], pt[1], f"S{i}", color='green', fontsize=9, ha='left', va='bottom')
        for i, (xr, yr) in enumerate(rebar_coords, start=1):
            ax.text(xr, yr, f"R{i}", color='red', fontsize=8, ha='left', va='bottom')

    # --- 5) Final plot formatting ---
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-10, width + 10)
    ax.set_ylim(-10, height + 10)
    ax.set_xlabel("X-axis (mm)")
    ax.set_ylabel("Y-axis (mm)")
    ax.set_title("Cross-Section with Rebar Layout")
    ax.legend()
    ax.grid(True)

    plt.show()


# =============================================================================
# Main Execution Block
# =============================================================================
if __name__ == "__main__":
    # Define section parameters
    width   = 300.0    # mm
    height  = 600.0    # mm
    cover   = 40.0     # mm (measured to stirrup outer face)
    ds      = 12.0     # mm (stirrup diameter)
    db      = 20.0     # mm (main bar diameter)
    nx      = 3        # number of bars along top & bottom
    ny      = 4        # number of bars along left & right

    # Compute the rebar coordinates and corners
    results = compute_rebar_coordinates(width, height, cover, ds, db, nx, ny)
    section_corners = results["section_corners"]
    stirrup_corners = results["stirrup_corners"]
    rebar_coords    = results["rebar_coords"]

    # Print the computed values
    print("Unconfined (outer) rectangle corners:")
    for i, corner in enumerate(section_corners, start=1):
        print(f"  C{i} = {corner}")

    print("\nConfined (inner) rectangle corners (center-line):")
    for i, corner in enumerate(stirrup_corners, start=1):
        print(f"  S{i} = {corner}")

    print("\nRebar coordinates:")
    for i, coord in enumerate(rebar_coords, start=1):
        print(f"  R{i} = {coord}")

    # Plot the cross-section with the rebar layout
    plot_beam_rebar(width, height, section_corners, stirrup_corners, rebar_coords, show_labels=True)

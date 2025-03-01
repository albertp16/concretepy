""" Section 418.6.4: Transverse Reinforcements """

def firsthoop (first_hoop_loc):
    if first_hoop_loc > 50:
        print(f"The first hoop should be within 50 mm of the face of the supporting member.")
        return False
    else:
        return True

def max_hoopspacing (depth, db, ds, hoopspacing):
    max_spacing = min(depth / 4, 6 * db, 24 * ds, 150)
    if hoopspacing > max_spacing:
        print(f"\nProvided hoop spacing exceeds the limit of {max_spacing}.")
        return False
    else:
        return True

""" Where hoops are not required - design according to 418.6.4.6 """
def hoops_not_required (depth, hoopspacing):
    max_spacing = depth / 2
    if hoopspacing > max_spacing:
        print(f"\nProvided hoop spacing exceeds the limit of {max_spacing}.")
        return False
    else:
        return True
    
def maxspacing (db, hoopspacing):
        max_spacing = min(6 * db, 150)
        if hoopspacing > max_spacing:
            print(f"Provided hoop spacing exceeds {max_spacing}.")
            return False
        else:
            return True    
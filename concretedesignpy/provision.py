def calculate_strength_reduction_factor(actual_epsilon, epsilon_ty, section_type):
    if not isinstance(actual_epsilon, (int, float)) or not isinstance(epsilon_ty, (int, float)):
        raise ValueError("actual_epsilon and epsilon_ty must be numbers.")
    if section_type not in ["spiral", "others"]:
        raise ValueError("section_type must be either 'spiral' or 'others'.")

    epsilon_t = 0.003 + epsilon_ty
    if actual_epsilon <= epsilon_ty:
        # compression-controlled
        phi = 0.75 if section_type == "spiral" else 0.65
    elif actual_epsilon < epsilon_t:
        # transition
        factor = (actual_epsilon - epsilon_ty) / 0.003
        if section_type == "spiral":
            phi = 0.75 + 0.15 * factor
        else:
            phi = 0.65 + 0.25 * factor
    else:
        # tension-controlled
        phi = 0.90
    return phi

def steel_yield_strain(fy, es):
    epsilon_s = fy / es
    return {
        "value": epsilon_s,
        "report": f"yield steel strain, epsilon_s = {epsilon_s:.6f}"
    }

def calculate_beta_one(fc):
    if fc < 17:
        raise ValueError("fc < 17 MPa is out of scope for this formula.")
    if 17 <= fc <= 28:
        beta_one = 0.85
        rep = "beta_1 = 0.85"
    elif 28 < fc < 55:
        beta_one = 0.85 - ((0.05 * (fc - 28)) / 7.0)
        rep = (f"beta_1 = 0.85 - (0.05*(fc - 28))/7\n"
               f"        = 0.85 - (0.05*({fc:.2f}-28))/7\n"
               f"        = {beta_one:.2f}")
    else:  # fc >= 55
        beta_one = 0.65
        rep = "beta_1 = 0.65"
    return {"value": beta_one, "report": rep}

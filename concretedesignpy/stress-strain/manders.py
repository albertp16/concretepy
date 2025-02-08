import numpy as np
import matplotlib.pyplot as plt


def compute_confined_strength(fpco: float, fpl: float) -> float:
    """
    Computes confined concrete strength using Mander's model.
    
    :param fpco: Unconfined concrete strength (MPa)
    :param fpl: Effective lateral confining stress (MPa)
    :return: Confined concrete strength (MPa)
    """
    A = 2.254 * np.sqrt(1 + ((7.92 * fpl) / fpco))
    B = 2 * (fpl / fpco)
    fpcc = fpco * (-1.254 + A - B)
    return fpcc


def compute_confined_strength_ratio(ratio: float) -> float:
    """
    Computes the confined strength ratio using lateral confinement stress ratio.
    
    :param ratio: Lateral confinement stress ratio (fpl / f'co)
    :return: Confined strength ratio (f'cc / f'co)
    """
    A = 2.254 * np.sqrt(1 + (7.92 * ratio))
    B = 2 * ratio
    return -1.254 + A - B


def compute_equation_A(r: float) -> float:
    """
    Computes coefficient A based on confinement ratio.
    
    :param r: Confinement stress ratio (fl1 / fl2)
    :return: Coefficient A
    """
    return 6.8886 - (0.6069 + (17.275 * r)) * np.exp(-4.989 * r)


def compute_equation_B(A: float, r: float) -> float:
    """
    Computes coefficient B based on coefficient A and ratio r.
    
    :param A: Coefficient A
    :param r: Confinement stress ratio (fl1 / fl2)
    :return: Coefficient B
    """
    B2 = ((5 / A) * (0.9849 - 0.6306 * np.exp(-3.8939 * r))) - 0.1
    return (4.5 / B2) - 5


def compute_confined_strength_factor(A: float, B: float, bar_x: float) -> float:
    """
    Computes confinement strength factor K.
    
    :param A: Coefficient A
    :param B: Coefficient B
    :param bar_x: Normalized confining stress (fl / f'co)
    :return: Confined strength factor K
    """
    return 1 + A * bar_x * (0.1 + (0.9 / (1 + B * bar_x)))


def solver(r: float, xi: float) -> float:
    """
    Computes the confined strength factor K.
    
    :param r: Confinement stress ratio (fl1 / fl2)
    :param xi: Normalized confinement stress
    :return: Confined strength factor K
    """
    A = compute_equation_A(r)
    B = compute_equation_B(A, r)
    k1 = A * (0.1 + 0.9 / (1 + (B * xi)))
    return 1 + (k1 * xi)


def plot_confined_strength():
    """
    Generates a plot of confined strength ratio vs. confinement stress ratio.
    """
    ratio_values = np.arange(0, 0.31, 0.01)
    value0 = [solver(0, r) for r in ratio_values]
    value1 = [solver(0.1, r) for r in ratio_values]
    value2 = [solver(0.2, r) for r in ratio_values]
    value_fl1_eq_fl2 = [compute_confined_strength_ratio(r) for r in ratio_values]
    
    # Plotting
    plt.figure(figsize=(8, 6))
    plt.plot(value0, -ratio_values, label="fl1/fl2 = 0")
    plt.plot(value1, -ratio_values, label="fl1/fl2 = 0.1")
    plt.plot(value2, -ratio_values, label="fl1/fl2 = 0.2")
    plt.plot(value_fl1_eq_fl2, -ratio_values, label="fl1 = fl2", linestyle='dashed')
    
    # Labels and Formatting
    plt.xlabel("Confined Strength Ratio, $f^{'}_{cc}/f^{'}_{co}$")
    plt.ylabel("Largest Confining Stress Ratio, $f^{'}_{l2}/f^{'}_{co}$")
    plt.title("Confined Strength Determination from Lateral Confining Stresses")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    plot_confined_strength()

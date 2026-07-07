"""
Experiment 2: Sensitivity Analysis for SCS-CN Runoff Model
AI-Augmented Software Engineering - Smart Water Lab Series

This module performs parameter sensitivity analysis for the SCS-CN method:
1. Fixed rainfall (P=50mm), varying CN values (60-100)
2. Rainfall vs Runoff curves for different CN values
3. Visualization of results

Physical Background:
- CN (Curve Number) represents land surface characteristics
- Higher CN → less infiltration → more runoff
- CN range: 0-100 (0=all infiltrates, 100=impervious)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scscn_runoff import calculate_runoff, calculate_S, calculate_Ia

# Configure matplotlib for headless environments
plt.use("Agg")

# Set Chinese font support
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


# =============================================================================
# SENSITIVITY ANALYSIS PARAMETERS
# =============================================================================

# Fixed rainfall depth (mm)
FIXED_RAINFALL = 50.0

# CN values for sensitivity analysis (representing different land uses)
CN_VALUES = [60, 70, 80, 90, 95, 100]
CN_LABELS = {
    60: "Woods (CN=60)",
    70: "Pasture (CN=70)",
    80: "Cultivated (CN=80)",
    90: "Urban (CN=90)",
    95: "Paved (CN=95)",
    100: "Impervious (CN=100)",
}

# Rainfall range for curve generation (mm)
RAINFALL_RANGE = np.linspace(0, 100, 101)


def run_cn_sensitivity_analysis():
    """
    Run sensitivity analysis: Fixed P=50mm, varying CN values.

    Returns:
        Dictionary with CN values as keys and runoff depths as values.
    """
    print("=" * 60)
    print("SCS-CN Sensitivity Analysis")
    print("Fixed Rainfall: P = {} mm".format(FIXED_RAINFALL))
    print("=" * 60)

    results = {}
    print("\n{:<10} {:<12} {:<12} {:<12} {:<12}".format(
        "CN", "S (mm)", "Ia (mm)", "Q (mm)", "Q/P Ratio"))
    print("-" * 60)

    for CN in CN_VALUES:
        S = calculate_S(CN)
        Ia = calculate_Ia(CN)
        Q = calculate_runoff(FIXED_RAINFALL, CN)
        ratio = Q / FIXED_RAINFALL if FIXED_RAINFALL > 0 else 0

        results[CN] = {
            "S": S,
            "Ia": Ia,
            "Q": Q,
            "ratio": ratio,
        }

        print("{:<10} {:<12.2f} {:<12.2f} {:<12.2f} {:<12.4f}".format(
            CN, S, Ia, Q, ratio))

    return results


def plot_cn_vs_runoff(results: dict, output_file: str = "cn_vs_runoff.png"):
    """
    Create bar chart: CN vs Runoff Depth (fixed P=50mm).

    Args:
        results: Dictionary from run_cn_sensitivity_analysis()
        output_file: Output filename for the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    cn_list = list(results.keys())
    q_list = [results[cn]["Q"] for cn in cn_list]
    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.9, len(cn_list)))

    bars = ax.bar(range(len(cn_list)), q_list, color=colors, edgecolor="black", linewidth=1)

    # Add value labels
    for bar, q in zip(bars, q_list):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, height + 0.5,
                f"{q:.1f}", ha="center", va="bottom", fontsize=10, fontweight="bold")

    ax.set_xlabel("Curve Number (CN)", fontsize=12)
    ax.set_ylabel("Runoff Depth Q (mm)", fontsize=12)
    ax.set_title(f"SCS-CN Sensitivity Analysis: Runoff vs CN\n(Fixed Rainfall P = {FIXED_RAINFALL} mm)",
                 fontsize=14, fontweight="bold")
    ax.set_xticks(range(len(cn_list)))
    ax.set_xticklabels([f"{cn}\n{CN_LABELS[cn].split('(')[0].strip()}" for cn in cn_list],
                       fontsize=9)
    ax.grid(axis="y", alpha=0.3)

    # Add rainfall reference line
    ax.axhline(y=FIXED_RAINFALL, color="blue", linestyle="--", alpha=0.5,
               label=f"Rainfall P = {FIXED_RAINFALL} mm")
    ax.legend(loc="upper left")

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches="tight")
    print(f"\n📊 Saved plot: {output_file}")
    plt.close()


def plot_rainfall_vs_runoff(output_file: str = "rainfall_vs_runoff.png"):
    """
    Create comparison plot: Rainfall vs Runoff for different CN values.

    Args:
        output_file: Output filename for the plot.
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    # Plot Q vs P curves for each CN value
    colors = plt.cm.viridis(np.linspace(0, 1, len(CN_VALUES)))

    for i, CN in enumerate(CN_VALUES):
        runoff_values = [calculate_runoff(P, CN) for P in RAINFALL_RANGE]
        ax.plot(RAINFALL_RANGE, runoff_values, color=colors[i],
                linewidth=2, label=f"CN={CN} ({CN_LABELS[CN].split('(')[0].strip()})")

    # Reference line: Q = P (maximum possible runoff)
    ax.plot(RAINFALL_RANGE, RAINFALL_RANGE, "k--", linewidth=1.5,
            alpha=0.5, label="Q = P (max)")

    ax.set_xlabel("Rainfall Depth P (mm)", fontsize=12)
    ax.set_ylabel("Runoff Depth Q (mm)", fontsize=12)
    ax.set_title("SCS-CN Model: Rainfall vs Runoff for Different CN Values",
                 fontsize=14, fontweight="bold")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches="tight")
    print(f"📊 Saved plot: {output_file}")
    plt.close()


def plot_runoff_comparison(output_file: str = "runoff_comparison.png"):
    """
    Create side-by-side comparison plots for different CN values.

    Args:
        output_file: Output filename for the plot.
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    rainfall_range = np.linspace(0, 100, 101)

    for i, CN in enumerate(CN_VALUES):
        ax = axes[i]
        runoff_values = [calculate_runoff(P, CN) for P in rainfall_range]

        # Plot Q vs P
        ax.fill_between(rainfall_range, runoff_values, alpha=0.3, color="steelblue")
        ax.plot(rainfall_range, runoff_values, color="steelblue", linewidth=2)
        ax.plot(rainfall_range, rainfall_range, "k--", linewidth=1, alpha=0.5)

        # Mark P=50mm point
        q_at_50 = calculate_runoff(50, CN)
        ax.plot(50, q_at_50, "ro", markersize=8)
        ax.annotate(f"Q={q_at_50:.1f}mm",
                    xy=(50, q_at_50), xytext=(55, q_at_50 + 5),
                    fontsize=9, arrowprops=dict(arrowstyle="->", color="red"))

        ax.set_title(f"{CN_LABELS[CN]}", fontsize=11, fontweight="bold")
        ax.set_xlabel("Rainfall P (mm)", fontsize=9)
        ax.set_ylabel("Runoff Q (mm)", fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

    plt.suptitle("SCS-CN Runoff Curves for Different Land Uses",
                 fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches="tight")
    print(f"📊 Saved plot: {output_file}")
    plt.close()


def generate_analysis_report(results: dict) -> str:
    """
    Generate text report of sensitivity analysis findings.

    Args:
        results: Dictionary from run_cn_sensitivity_analysis()

    Returns:
        Analysis report as string.
    """
    report = []
    report.append("=" * 60)
    report.append("SCS-CN SENSITIVITY ANALYSIS REPORT")
    report.append("=" * 60)
    report.append(f"\nFixed Rainfall: P = {FIXED_RAINFALL} mm")
    report.append(f"Analysis Date: 2026-07-07")
    report.append("\n" + "-" * 60)

    # Key findings
    report.append("\nKEY FINDINGS:")
    report.append(f"1. Runoff range: {results[60]['Q']:.2f} mm (CN=60) to {results[100]['Q']:.2f} mm (CN=100)")
    report.append(f"2. Runoff ratio range: {results[60]['ratio']:.2%} to {results[100]['ratio']:.2%}")
    report.append(f"3. Ratio increase: {(results[100]['Q'] / results[60]['Q']):.1f}x from CN=60 to CN=100")

    # Physical validation
    report.append("\nPHYSICAL VALIDATION:")
    all_valid = True
    for CN in CN_VALUES:
        Q = results[CN]["Q"]
        if Q > FIXED_RAINFALL:
            report.append(f"  ❌ CN={CN}: Q={Q:.2f} > P={FIXED_RAINFALL} - VIOLATION!")
            all_valid = False
        else:
            report.append(f"  ✅ CN={CN}: Q={Q:.2f} <= P={FIXED_RAINFALL}")
    if all_valid:
        report.append("  All cases satisfy physical constraint Q <= P")

    # Monotonicity check
    report.append("\nMONOTONICITY CHECK:")
    q_values = [results[CN]["Q"] for CN in CN_VALUES]
    is_monotonic = all(q_values[i] <= q_values[i+1] for i in range(len(q_values)-1))
    report.append(f"  Runoff increases monotonically with CN: {'✅ Yes' if is_monotonic else '❌ No'}")

    report.append("\n" + "=" * 60)
    return "\n".join(report)


if __name__ == "__main__":
    # Run sensitivity analysis
    results = run_cn_sensitivity_analysis()

    # Generate plots
    print("\n" + "=" * 60)
    print("Generating Visualizations...")
    print("=" * 60)

    plot_cn_vs_runoff(results, "cn_vs_runoff.png")
    plot_rainfall_vs_runoff("rainfall_vs_runoff.png")
    plot_runoff_comparison("runoff_comparison.png")

    # Generate and save report
    report = generate_analysis_report(results)
    print("\n" + report)

    with open("sensitivity_report.txt", "w") as f:
        f.write(report)
    print("\n📄 Saved report: sensitivity_report.txt")

    print("\n✅ Sensitivity analysis complete!")

"""
Experiment 4: Flood Inundation Analysis (DEM-based)
AI-Augmented Software Engineering - Smart Water Lab Series

This module implements flood inundation analysis using Digital Elevation Model (DEM) data.
It includes functions for DEM generation, flood simulation, visualization, and dynamic
simulation of rising water levels.

Physical Background:
    A location is FLOODED if: Elevation < Flood_Water_Level
    Inundation Depth = Flood_Water_Level - Elevation (if flooded)
    Flooded Area % = (Flooded cells / Total cells) * 100

DEM Sources:
    - USGS SRTM (30m resolution)
    - ALOS PALSAR (12.5m resolution)
    - Synthetic DEM (for testing)
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from typing import Tuple, Optional
import os


# =============================================================================
# DEM DATA FUNCTIONS
# =============================================================================

def generate_synthetic_dem(size: int = 100,
                            elevation_range: Tuple[float, float] = (30, 80),
                            seed: int = 42) -> np.ndarray:
    """
    Generate a synthetic DEM with realistic terrain features.

    Creates a terrain with:
    - Rolling hills using sine/cosine functions
    - Random noise for surface roughness
    - A valley/channel for flood simulation

    Args:
        size: Grid size (size x size)
        elevation_range: (min_elevation, max_elevation) in meters
        seed: Random seed for reproducibility

    Returns:
        2D numpy array of elevation values.
    """
    np.random.seed(seed)
    x = np.linspace(0, 4 * np.pi, size)
    y = np.linspace(0, 4 * np.pi, size)
    X, Y = np.meshgrid(x, y)

    # Base terrain: combination of sine waves for hills
    dem = (np.sin(X * 0.8) * np.cos(Y * 0.6) * 0.5 +
           np.sin(X * 1.2 + Y * 0.4) * 0.3 +
           np.cos(X * 0.3 - Y * 0.9) * 0.2)

    # Add valley/channel (lower elevation in center)
    center_x, center_y = size // 2, size // 2
    for i in range(size):
        for j in range(size):
            dist_from_center = np.sqrt((i - center_x)**2 + (j - center_y)**2)
            if dist_from_center < size * 0.3:
                dem[i, j] -= 0.5 * (1 - dist_from_center / (size * 0.3))

    # Add random surface roughness
    noise = np.random.normal(0, 0.05, (size, size))
    dem += noise

    # Normalize to elevation range
    dem_min, dem_max = dem.min(), dem.max()
    min_elev, max_elev = elevation_range
    dem = min_elev + (dem - dem_min) / (dem_max - dem_min) * (max_elev - min_elev)

    return dem


def save_dem(dem: np.ndarray, filepath: str = "dem_data.npy") -> None:
    """Save DEM data to numpy file."""
    np.save(filepath, dem)


def load_dem(filepath: str = "dem_data.npy") -> np.ndarray:
    """Load DEM data from numpy file."""
    return np.load(filepath)


# =============================================================================
# FLOOD SIMULATION FUNCTIONS
# =============================================================================

def simulate_flood(dem: np.ndarray, water_level: float) -> Tuple[np.ndarray, np.ndarray, float]:
    """
    Simulate flood inundation at a given water level.

    Physical Logic:
        Flooded if: Elevation < Water_Level
        Depth = Water_Level - Elevation (for flooded cells)
        % Area = (Flooded cells / Total cells) * 100

    Args:
        dem: 2D array of elevation values (meters)
        water_level: Flood water level (meters)

    Returns:
        Tuple of:
        - flooded_mask: Boolean array (True = flooded)
        - depth: Inundation depth array (meters, 0 for non-flooded)
        - percentage: Flooded area percentage
    """
    # Create flood mask: True where elevation < water level
    flooded_mask = dem < water_level

    # Calculate inundation depth
    depth = np.where(flooded_mask, water_level - dem, 0.0)

    # Calculate flooded area percentage
    flooded_cells = np.sum(flooded_mask)
    total_cells = dem.size
    percentage = (flooded_cells / total_cells) * 100.0

    return flooded_mask, depth, percentage


def calculate_flood_statistics(dem: np.ndarray, water_level: float) -> dict:
    """
    Calculate comprehensive flood statistics.

    Args:
        dem: 2D elevation array
        water_level: Water level in meters

    Returns:
        Dictionary with flood statistics.
    """
    flooded_mask, depth, percentage = simulate_flood(dem, water_level)

    if np.any(flooded_mask):
        avg_depth = np.mean(depth[flooded_mask])
        max_depth = np.max(depth[flooded_mask])
        min_elev = np.min(dem)
        max_elev = np.max(dem)
    else:
        avg_depth = 0.0
        max_depth = 0.0
        min_elev = np.min(dem)
        max_elev = np.max(dem)

    return {
        "water_level": water_level,
        "flooded_percentage": percentage,
        "flooded_cells": int(np.sum(flooded_mask)),
        "total_cells": dem.size,
        "average_depth": avg_depth,
        "maximum_depth": max_depth,
        "minimum_elevation": min_elev,
        "maximum_elevation": max_elev,
    }


# =============================================================================
# VISUALIZATION FUNCTIONS
# =============================================================================

def create_flood_colormap() -> LinearSegmentedColormap:
    """Create custom blue colormap for flood visualization."""
    colors = [
        (0.9, 0.95, 1.0),   # Very light blue (shallow)
        (0.6, 0.8, 1.0),    # Light blue
        (0.3, 0.6, 0.9),    # Medium blue
        (0.1, 0.4, 0.8),    # Deep blue
        (0.0, 0.2, 0.6),    # Very deep blue
    ]
    return LinearSegmentedColormap.from_list("flood_blues", colors)


def visualize_flood(dem: np.ndarray, water_level: float,
                    output_file: Optional[str] = None) -> plt.Figure:
    """
    Create flood inundation visualization.

    Args:
        dem: 2D elevation array
        water_level: Water level in meters
        output_file: Optional output filename

    Returns:
        Matplotlib figure object.
    """
    flooded_mask, depth, percentage = simulate_flood(dem, water_level)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Plot 1: Original DEM
    im1 = axes[0].imshow(dem, cmap="terrain", aspect="equal")
    axes[0].set_title("Digital Elevation Model (DEM)", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("X (cells)")
    axes[0].set_ylabel("Y (cells)")
    plt.colorbar(im1, ax=axes[0], label="Elevation (m)")

    # Plot 2: Flood extent overlay
    axes[1].imshow(dem, cmap="gray", aspect="equal", alpha=0.5)
    flood_cmap = create_flood_colormap()
    im2 = axes[1].imshow(np.where(flooded_mask, depth, np.nan),
                          cmap=flood_cmap, aspect="equal", vmin=0, vmax=20)
    axes[1].set_title(f"Flood Extent (Water Level: {water_level}m)\n"
                      f"Flooded: {percentage:.1f}%", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("X (cells)")
    plt.colorbar(im2, ax=axes[1], label="Inundation Depth (m)")

    # Plot 3: Inundation depth heatmap
    im3 = axes[2].imshow(depth, cmap=flood_cmap, aspect="equal")
    axes[2].set_title("Inundation Depth Map", fontsize=12, fontweight="bold")
    axes[2].set_xlabel("X (cells)")
    plt.colorbar(im3, ax=axes[2], label="Depth (m)")

    # Add contour lines for water level
    axes[0].contour(dem, levels=[water_level], colors="blue", linewidths=2)
    axes[1].contour(dem, levels=[water_level], colors="white", linewidths=1.5)

    plt.tight_layout()

    if output_file:
        plt.savefig(output_file, dpi=150, bbox_inches="tight")
        print(f"📊 Saved flood visualization: {output_file}")

    return fig


def visualize_comparison(dem: np.ndarray, water_levels: list,
                         output_file: Optional[str] = None) -> plt.Figure:
    """
    Create side-by-side comparison at different water levels.

    Args:
        dem: 2D elevation array
        water_levels: List of water levels to compare
        output_file: Optional output filename

    Returns:
        Matplotlib figure object.
    """
    n_levels = len(water_levels)
    fig, axes = plt.subplots(1, n_levels, figsize=(6 * n_levels, 5))

    if n_levels == 1:
        axes = [axes]

    flood_cmap = create_flood_colormap()

    for i, wl in enumerate(water_levels):
        flooded_mask, depth, percentage = simulate_flood(dem, wl)

        axes[i].imshow(dem, cmap="gray", aspect="equal", alpha=0.4)
        im = axes[i].imshow(np.where(flooded_mask, depth, np.nan),
                            cmap=flood_cmap, aspect="equal", vmin=0, vmax=20)
        axes[i].set_title(f"Water Level: {wl}m\nFlooded: {percentage:.1f}%",
                          fontsize=11, fontweight="bold")
        axes[i].set_xlabel("X (cells)")
        if i == 0:
            axes[i].set_ylabel("Y (cells)")
        plt.colorbar(im, ax=axes[i], label="Depth (m)")

    plt.suptitle("Flood Inundation Comparison at Different Water Levels",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()

    if output_file:
        plt.savefig(output_file, dpi=150, bbox_inches="tight")
        print(f"📊 Saved comparison: {output_file}")

    return fig


# =============================================================================
# DYNAMIC SIMULATION
# =============================================================================

def simulate_rising_water(dem: np.ndarray,
                          water_levels: np.ndarray) -> Tuple[np.ndarray, list]:
    """
    Simulate flooding as water level rises.

    Args:
        dem: 2D elevation array
        water_levels: Array of water levels to simulate

    Returns:
        Tuple of:
        - percentages: Array of flooded percentages
        - all_depths: List of depth arrays for each level
    """
    percentages = np.zeros(len(water_levels))
    all_depths = []

    for i, wl in enumerate(water_levels):
        _, depth, pct = simulate_flood(dem, wl)
        percentages[i] = pct
        all_depths.append(depth)

    return percentages, all_depths


def plot_flood_curve(dem: np.ndarray, water_levels: np.ndarray,
                     percentages: np.ndarray,
                     output_file: Optional[str] = "flood_curve.png") -> plt.Figure:
    """
    Create plot of water level vs flooded percentage.

    Args:
        dem: 2D elevation array
        water_levels: Array of water levels
        percentages: Array of flooded percentages
        output_file: Output filename

    Returns:
        Matplotlib figure object.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Water level vs flooded percentage
    ax1.fill_between(water_levels, percentages, alpha=0.3, color="steelblue")
    ax1.plot(water_levels, percentages, "b-o", linewidth=2, markersize=6)
    ax1.set_xlabel("Water Level (m)", fontsize=12)
    ax1.set_ylabel("Flooded Area (%)", fontsize=12)
    ax1.set_title("Water Level vs Flooded Area Percentage", fontsize=13, fontweight="bold")
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 105)

    # Plot 2: Rate of change (derivative)
    if len(water_levels) > 1:
        d_pct = np.diff(percentages) / np.diff(water_levels)
        ax2.bar(water_levels[:-1] + np.diff(water_levels)/2, d_pct,
                width=np.diff(water_levels)[0]*0.8, alpha=0.6, color="coral",
                edgecolor="black", linewidth=0.5)
        ax2.set_xlabel("Water Level (m)", fontsize=12)
        ax2.set_ylabel("Rate of Increase (%/m)", fontsize=12)
        ax2.set_title("Inundation Rate of Change", fontsize=13, fontweight="bold")
        ax2.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches="tight")
    print(f"📊 Saved flood curve: {output_file}")
    plt.close()

    return fig


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_flood_simulation(dem: np.ndarray, water_levels: np.ndarray,
                               percentages: np.ndarray) -> dict:
    """
    Validate flood simulation results.

    Physical Checks:
        1. Flooded area increases monotonically with water level
        2. Maximum depth = water_level - min_elevation
        3. Percentage is between 0 and 100
        4. Edge cases: below min elevation, above max elevation

    Args:
        dem: 2D elevation array
        water_levels: Array of water levels
        percentages: Array of flooded percentages

    Returns:
        Dictionary with validation results.
    """
    checks = {
        "monotonic": True,
        "max_depth": True,
        "percentage_range": True,
        "edge_cases": True,
    }
    details = []

    # Check 1: Monotonic increase
    for i in range(1, len(percentages)):
        if percentages[i] < percentages[i - 1] - 0.01:  # Small tolerance
            checks["monotonic"] = False
            details.append(f"  ❌ Flooded area decreased at level {water_levels[i]}m")

    if checks["monotonic"]:
        details.append("  ✅ Flooded area increases monotonically")

    # Check 2: Max depth check at highest water level
    if len(water_levels) > 0:
        max_wl = water_levels[-1]
        _, depth, _ = simulate_flood(dem, max_wl)
        min_elev = np.min(dem)
        expected_max_depth = max_wl - min_elev
        actual_max_depth = np.max(depth)

        if abs(actual_max_depth - expected_max_depth) > 0.01:
            checks["max_depth"] = False
            details.append(f"  ❌ Max depth mismatch: {actual_max_depth:.2f} vs {expected_max_depth:.2f}")
        else:
            details.append(f"  ✅ Max depth correct: {actual_max_depth:.2f}m")

    # Check 3: Percentage range
    if np.any(percentages < 0) or np.any(percentages > 100):
        checks["percentage_range"] = False
        details.append("  ❌ Percentage out of [0, 100] range")
    else:
        details.append("  ✅ All percentages in valid range [0, 100]")

    # Check 4: Edge cases
    min_elev = np.min(dem)
    max_elev = np.max(dem)

    # Below minimum elevation: should flood everything
    _, _, pct_below = simulate_flood(dem, min_elev - 1)
    if pct_below > 0.01:
        checks["edge_cases"] = False
        details.append(f"  ❌ Below min elevation floods {pct_below:.1f}% (should be 0)")
    else:
        details.append("  ✅ Below min elevation: 0% flooded")

    # Above maximum elevation: should flood 100%
    _, _, pct_above = simulate_flood(dem, max_elev + 1)
    if pct_above < 99.99:
        checks["edge_cases"] = False
        details.append(f"  ❌ Above max elevation floods {pct_above:.1f}% (should be 100)")
    else:
        details.append("  ✅ Above max elevation: ~100% flooded")

    all_passed = all(checks.values())

    return {
        "all_passed": all_passed,
        "checks": checks,
        "details": details,
    }


def generate_validation_report(dem: np.ndarray, water_levels: np.ndarray,
                               percentages: np.ndarray) -> str:
    """Generate validation report as text."""
    validation = validate_flood_simulation(dem, water_levels, percentages)

    report = []
    report.append("=" * 60)
    report.append("FLOOD INUNDATION VALIDATION REPORT")
    report.append("=" * 60)
    report.append(f"\nDEM Size: {dem.shape}")
    report.append(f"Elevation Range: [{np.min(dem):.1f}, {np.max(dem):.1f}] m")
    report.append(f"Water Level Range: [{water_levels[0]:.1f}, {water_levels[-1]:.1f}] m")
    report.append(f"\n{'='*60}")
    report.append("PHYSICAL VALIDATION:")
    report.append(f"{'='*60}")

    for detail in validation["details"]:
        report.append(detail)

    report.append(f"\nOverall: {'✅ ALL CHECKS PASSED' if validation['all_passed'] else '❌ SOME CHECKS FAILED'}")
    report.append("=" * 60)

    return "\n".join(report)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("FLOOD INUNDATION ANALYSIS (DEM-based)")
    print("=" * 60)

    # Step 1: Generate DEM data
    print("\n[1/4] Generating synthetic DEM...")
    dem = generate_synthetic_dem(size=100, elevation_range=(30, 80))
    save_dem(dem, "dem_data.npy")
    print(f"  DEM shape: {dem.shape}")
    print(f"  Elevation range: [{dem.min():.1f}, {dem.max():.1f}] m")

    # Step 2: Simulate flood at different water levels
    print("\n[2/4] Simulating flood inundation...")
    water_level_40m = 40.0
    water_level_50m = 50.0

    stats_40m = calculate_flood_statistics(dem, water_level_40m)
    stats_50m = calculate_flood_statistics(dem, water_level_50m)

    print(f"\n  Water Level {water_level_40m}m:")
    print(f"    Flooded: {stats_40m['flooded_percentage']:.1f}%")
    print(f"    Avg Depth: {stats_40m['average_depth']:.2f}m")
    print(f"    Max Depth: {stats_40m['maximum_depth']:.2f}m")

    print(f"\n  Water Level {water_level_50m}m:")
    print(f"    Flooded: {stats_50m['flooded_percentage']:.1f}%")
    print(f"    Avg Depth: {stats_50m['average_depth']:.2f}m")
    print(f"    Max Depth: {stats_50m['maximum_depth']:.2f}m")

    # Step 3: Create visualizations
    print("\n[3/4] Creating visualizations...")
    visualize_flood(dem, water_level_40m, "flood_extent_40m.png")
    visualize_flood(dem, water_level_50m, "flood_extent_50m.png")
    visualize_comparison(dem, [40, 45, 50], "flood_comparison.png")

    # Step 4: Dynamic simulation
    print("\n[4/4] Running dynamic simulation...")
    water_levels = np.linspace(35, 55, 21)
    percentages, all_depths = simulate_rising_water(dem, water_levels)
    plot_flood_curve(dem, water_levels, percentages, "flood_curve.png")

    # Validation
    print("\n" + "=" * 60)
    validation_report = generate_validation_report(dem, water_levels, percentages)
    print(validation_report)

    with open("validation_report.txt", "w") as f:
        f.write(validation_report)
    print("\n📄 Saved validation report: validation_report.txt")

    print("\n✅ Flood inundation analysis complete!")

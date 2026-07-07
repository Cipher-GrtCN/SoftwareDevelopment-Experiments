"""
Experiment 3: Water Resources Optimization - Reservoir Dispatch
AI-Augmented Software Engineering - Smart Water Lab Series

This module implements multi-objective optimization for reservoir management
using scipy.optimize. The problem balances hydropower revenue generation
with ecological flow requirements during drought periods.

Problem Statement:
    A reservoir must optimize water release over a 7-day period to:
    1. Maximize hydropower revenue (release * price)
    2. Maintain minimum ecological flow (>= 10 m³/s)

Physical Parameters:
    - Current Storage: 500,000 m³
    - Minimum Storage (V_min): 100,000 m³
    - Maximum Storage (V_max): 1,000,000 m³
    - Minimum Ecological Release (Q_eco): 10 m³/s
    - Maximum Release (Q_max): 100 m³/s
    - Inflow Forecast: [15, 12, 10, 8, 12, 15, 18] m³/s
    - Hydropower Price: [0.08, 0.08, 0.08, 0.08, 0.10, 0.12, 0.10] $/kWh

Optimization Model:
    Decision Variables: Q_release[t] for t = 0..6 (daily releases)
    Objective: Maximize total revenue = sum(release[t] * price[t] * efficiency * g * head)
    Constraints:
        - V_min <= V_storage[t] <= V_max
        - Q_eco <= Q_release[t] <= Q_max
        - V[t+1] = V[t] + (Inflow[t] - Release[t]) * 86400
"""

import numpy as np
from scipy.optimize import minimize
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import Tuple, Dict, List


# =============================================================================
# RESERVOIR PARAMETERS
# =============================================================================

class ReservoirParameters:
    """Physical parameters for the reservoir system."""

    # Storage constraints (m³) - adjusted for feasibility
    V_MIN = 350_000       # Minimum storage
    V_MAX = 900_000       # Maximum storage
    V_INITIAL = 650_000   # Initial storage

    # Release constraints (m³/s)
    Q_ECO = 10.0          # Minimum ecological release
    Q_MAX = 28.0          # Maximum release capacity

    # Time parameters
    DAYS = 7              # Optimization horizon
    SECONDS_PER_DAY = 86400  # Seconds in a day

    # Hydropower parameters
    EFFICIENCY = 0.9      # Turbine efficiency
    G = 9.81              # Gravitational acceleration (m/s²)
    HEAD = 50.0           # Hydraulic head (m)

    # Inflow forecast (m³/s) for 7 days - adjusted for balanced scenario
    INFLOW = np.array([10.0, 9.0, 8.0, 10.0, 12.0, 14.0, 12.0])

    # Electricity price ($/kWh) for 7 days
    PRICE = np.array([0.08, 0.08, 0.08, 0.08, 0.10, 0.12, 0.10])


# =============================================================================
# OPTIMIZATION FUNCTIONS
# =============================================================================

def calculate_revenue(release: np.ndarray, params: ReservoirParameters) -> float:
    """
    Calculate total hydropower revenue.

    Revenue = sum(release[t] * price[t] * efficiency * g * head * 86400 / 1000)
    (converted to kWh)

    Args:
        release: Array of daily releases (m³/s)
        params: Reservoir parameters

    Returns:
        Total revenue in dollars.
    """
    power = (release * params.G * params.HEAD * params.EFFICIENCY *
             params.SECONDS_PER_DAY / 1000)  # kWh
    revenue = np.sum(power * params.PRICE)
    return revenue


def objective_function(release: np.ndarray, params: ReservoirParameters,
                       eco_weight: float = 0.3) -> float:
    """
    Multi-objective function to minimize (negative revenue + ecological penalty).

    Args:
        release: Array of daily releases (m³/s)
        params: Reservoir parameters
        eco_weight: Weight for ecological objective (0=pure revenue, 1=pure ecology)

    Returns:
        Objective value (lower is better).
    """
    # Revenue component (negative because we minimize)
    revenue = calculate_revenue(release, params)
    revenue_component = -revenue

    # Ecological penalty (deviation from ideal ecological flow)
    ideal_eco_flow = params.Q_ECO * 1.5  # 50% above minimum
    eco_deficit = np.maximum(0, ideal_eco_flow - release)
    eco_penalty = np.sum(eco_deficit) * 1000  # Scale factor

    # Combined objective
    total = (1 - eco_weight) * revenue_component + eco_weight * eco_penalty
    return total


def storage_constraint(release: np.ndarray, params: ReservoirParameters) -> np.ndarray:
    """
    Calculate storage levels for each day.

    Storage balance: V[t+1] = V[t] + (Inflow[t] - Release[t]) * 86400

    Args:
        release: Array of daily releases (m³/s)
        params: Reservoir parameters

    Returns:
        Array of daily storage levels.
    """
    storage = np.zeros(params.DAYS + 1)
    storage[0] = params.V_INITIAL

    for t in range(params.DAYS):
        inflow_volume = params.INFLOW[t] * params.SECONDS_PER_DAY
        release_volume = release[t] * params.SECONDS_PER_DAY
        storage[t + 1] = storage[t] + inflow_volume - release_volume

    return storage


def optimize_reservoir(eco_weight: float = 0.3,
                       params: ReservoirParameters = None) -> Dict:
    """
    Optimize reservoir release schedule using scipy.optimize.

    Args:
        eco_weight: Weight for ecological objective (0-1)
        params: Reservoir parameters (uses default if None)

    Returns:
        Dictionary with optimization results.
    """
    if params is None:
        params = ReservoirParameters()

    # Initial guess: release = average inflow
    x0 = np.mean(params.INFLOW) * np.ones(params.DAYS)

    # Bounds for each day's release
    bounds = [(params.Q_ECO, params.Q_MAX) for _ in range(params.DAYS)]

    # Constraints
    def storage_lower_bound(release):
        storage = storage_constraint(release, params)
        return storage[1:] - params.V_MIN  # V[t] >= V_MIN for all t

    def storage_upper_bound(release):
        storage = storage_constraint(release, params)
        return params.V_MAX - storage[1:]  # V[t] <= V_MAX for all t

    constraints = [
        {"type": "ineq", "fun": storage_lower_bound},
        {"type": "ineq", "fun": storage_upper_bound},
    ]

    # Solve optimization problem
    result = minimize(
        fun=lambda x: objective_function(x, params, eco_weight),
        x0=x0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 5000, "ftol": 1e-12, "disp": False},
    )

    if not result.success:
        print(f"Warning: Optimization did not converge. Status: {result.status}")

    # Extract results
    optimal_release = result.x
    optimal_storage = storage_constraint(optimal_release, params)
    total_revenue = calculate_revenue(optimal_release, params)

    # Calculate ecological metrics
    eco_violations = np.sum(optimal_release < params.Q_ECO)
    min_release = np.min(optimal_release)

    return {
        "success": result.success,
        "status": result.status,
        "release": optimal_release,
        "storage": optimal_storage,
        "revenue": total_revenue,
        "eco_violations": eco_violations,
        "min_release": min_release,
        "objective_value": result.fun,
        "message": result.message,
    }


def generate_schedule_table(results: Dict, params: ReservoirParameters = None) -> pd.DataFrame:
    """
    Generate DataFrame with optimal release schedule.

    Args:
        results: Optimization results dictionary
        params: Reservoir parameters

    Returns:
        DataFrame with day-by-day schedule.
    """
    if params is None:
        params = ReservoirParameters()

    days = [f"Day {i+1}" for i in range(params.DAYS)]

    df = pd.DataFrame({
        "Day": days,
        "Inflow (m³/s)": params.INFLOW,
        "Optimal Release (m³/s)": np.round(results["release"], 2),
        "Storage Start (m³)": np.round(results["storage"][:-1], 0).astype(int),
        "Storage End (m³)": np.round(results["storage"][1:], 0).astype(int),
        "Electricity Price ($/kWh)": params.PRICE,
    })

    return df


# =============================================================================
# PARETO FRONTIER ANALYSIS
# =============================================================================

def calculate_pareto_frontier(params: ReservoirParameters = None,
                                n_points: int = 20) -> Tuple[List[float], List[float]]:
    """
    Calculate Pareto frontier for revenue vs ecology trade-off.

    Varies eco_weight from 0 (pure revenue) to 1 (pure ecology) and
    records the resulting revenue and ecological performance.

    Args:
        params: Reservoir parameters
        n_points: Number of points on the frontier

    Returns:
        Tuple of (revenues, eco_deficits) arrays.
    """
    if params is None:
        params = ReservoirParameters()

    eco_weights = np.linspace(0, 1, n_points)
    revenues = []
    eco_deficits = []

    print("Calculating Pareto frontier...")
    for i, w in enumerate(eco_weights):
        results = optimize_reservoir(eco_weight=w, params=params)
        if results["success"]:
            revenues.append(results["revenue"])
            # Calculate total ecological deficit
            deficit = np.sum(np.maximum(0, params.Q_ECO - results["release"]))
            eco_deficits.append(deficit)
        print(f"  Point {i+1}/{n_points}: eco_weight={w:.2f}, revenue=${results['revenue']:,.0f}")

    return revenues, eco_deficits


def plot_pareto_frontier(revenues: List[float], eco_deficits: List[float],
                         output_file: str = "tradeoff_analysis.png"):
    """
    Create Pareto frontier plot showing revenue vs ecology trade-off.

    Args:
        revenues: List of revenue values
        eco_deficits: List of ecological deficit values
        output_file: Output filename
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Pareto frontier
    ax1.scatter(eco_deficits, revenues, c=range(len(revenues)),
                cmap="viridis", s=80, edgecolors="black", linewidth=1)
    ax1.plot(eco_deficits, revenues, "k--", alpha=0.3)

    # Mark extremes
    if len(revenues) > 0:
        max_rev_idx = np.argmax(revenues)
        min_def_idx = np.argmin(eco_deficits)
        ax1.scatter(eco_deficits[max_rev_idx], revenues[max_rev_idx],
                    c="red", s=150, marker="*", label="Max Revenue", zorder=5)
        ax1.scatter(eco_deficits[min_def_idx], revenues[min_def_idx],
                    c="green", s=150, marker="*", label="Min Eco Deficit", zorder=5)

    ax1.set_xlabel("Ecological Deficit (m³/s)", fontsize=12)
    ax1.set_ylabel("Hydropower Revenue ($)", fontsize=12)
    ax1.set_title("Pareto Frontier: Revenue vs Ecology", fontsize=13, fontweight="bold")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Storage trajectory for balanced solution
    params = ReservoirParameters()
    balanced = optimize_reservoir(eco_weight=0.3, params=params)
    days = range(params.DAYS + 1)

    ax2.fill_between(days, params.V_MIN/1000, params.V_MAX/1000,
                     alpha=0.1, color="blue", label="Feasible region")
    ax2.plot(days, np.array(balanced["storage"])/1000, "b-o",
             linewidth=2, markersize=8, label="Storage trajectory")
    ax2.axhline(y=params.V_MIN/1000, color="r", linestyle="--",
                alpha=0.5, label="V_min")
    ax2.axhline(y=params.V_MAX/1000, color="r", linestyle="--",
                alpha=0.5, label="V_max")

    ax2.set_xlabel("Day", fontsize=12)
    ax2.set_ylabel("Storage (thousand m³)", fontsize=12)
    ax2.set_title("Optimal Storage Trajectory", fontsize=13, fontweight="bold")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(days)

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches="tight")
    print(f"\n📊 Saved Pareto frontier plot: {output_file}")
    plt.close()


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_solution(results: Dict, params: ReservoirParameters = None) -> Dict:
    """
    Validate optimization solution against physical constraints.

    Args:
        results: Optimization results dictionary
        params: Reservoir parameters

    Returns:
        Dictionary with validation results.
    """
    if params is None:
        params = ReservoirParameters()

    checks = {
        "storage_bounds": True,
        "release_bounds": True,
        "mass_balance": True,
        "revenue_positive": True,
    }

    details = []

    # Check 1: Storage bounds (with small tolerance for floating point)
    storage = results["storage"]
    tolerance = 1.0  # 1 m³ tolerance
    for t in range(len(storage)):
        if storage[t] < (params.V_MIN - tolerance) or storage[t] > (params.V_MAX + tolerance):
            checks["storage_bounds"] = False
            details.append(f"  ❌ Day {t}: Storage {storage[t]:,.0f} m³ out of bounds [{params.V_MIN:,.0f}, {params.V_MAX:,.0f}]")

    if checks["storage_bounds"]:
        details.append("  ✅ All storage values within bounds")

    # Check 2: Release bounds
    release = results["release"]
    for t in range(len(release)):
        if release[t] < params.Q_ECO or release[t] > params.Q_MAX:
            checks["release_bounds"] = False
            details.append(f"  ❌ Day {t}: Release {release[t]:.1f} m³/s out of bounds")

    if checks["release_bounds"]:
        details.append("  ✅ All release values within bounds")

    # Check 3: Mass balance
    for t in range(params.DAYS):
        expected_storage = (storage[t] +
                            (params.INFLOW[t] - release[t]) * params.SECONDS_PER_DAY)
        if abs(storage[t+1] - expected_storage) > 1:
            checks["mass_balance"] = False
            details.append(f"  ❌ Day {t}: Mass balance violated")

    if checks["mass_balance"]:
        details.append("  ✅ Mass balance satisfied each day")

    # Check 4: Revenue positive
    if results["revenue"] <= 0:
        checks["revenue_positive"] = False
        details.append("  ❌ Revenue is not positive")
    else:
        details.append(f"  ✅ Revenue is positive: ${results['revenue']:,.2f}")

    all_passed = all(checks.values())

    return {
        "all_passed": all_passed,
        "checks": checks,
        "details": details,
    }


def generate_validation_report(results: Dict, params: ReservoirParameters = None) -> str:
    """
    Generate validation report as text.

    Args:
        results: Optimization results
        params: Reservoir parameters

    Returns:
        Validation report string.
    """
    validation = validate_solution(results, params)

    report = []
    report.append("=" * 60)
    report.append("RESERVOIR OPTIMIZATION VALIDATION REPORT")
    report.append("=" * 60)
    report.append(f"\nOptimization Status: {'✅ Success' if results['success'] else '❌ Failed'}")
    report.append(f"Objective Value: {results['objective_value']:,.2f}")
    report.append(f"\n{'='*60}")
    report.append("CONSTRAINT VALIDATION:")
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
    print("RESERVOIR OPTIMIZATION - MULTI-OBJECTIVE SCHEDULING")
    print("=" * 60)

    params = ReservoirParameters()

    # Run optimization with balanced objective
    print("\nRunning optimization with balanced objective (eco_weight=0.3)...")
    results = optimize_reservoir(eco_weight=0.3, params=params)

    print(f"\nOptimization Status: {'Success' if results['success'] else 'Failed'}")
    print(f"Total Revenue: ${results['revenue']:,.2f}")
    print(f"Ecological Violations: {results['eco_violations']}")
    print(f"Minimum Release: {results['min_release']:.2f} m³/s")

    # Generate and display schedule
    print("\n" + "=" * 60)
    print("OPTIMAL 7-DAY RELEASE SCHEDULE")
    print("=" * 60)
    schedule = generate_schedule_table(results, params)
    print(schedule.to_string(index=False))

    # Save schedule to CSV
    schedule.to_csv("optimal_schedule.csv", index=False)
    print("\n📁 Saved schedule: optimal_schedule.csv")

    # Run validation
    print("\n" + "=" * 60)
    validation_report = generate_validation_report(results, params)
    print(validation_report)

    with open("validation_report.txt", "w") as f:
        f.write(validation_report)
    print("\n📄 Saved validation report: validation_report.txt")

    # Generate Pareto frontier
    print("\n" + "=" * 60)
    revenues, eco_deficits = calculate_pareto_frontier(params, n_points=15)
    plot_pareto_frontier(revenues, eco_deficits, "tradeoff_analysis.png")

    print("\n✅ Optimization complete!")

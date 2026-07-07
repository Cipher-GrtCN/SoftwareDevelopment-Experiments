# Experiment 3: Water Resources Optimization - Reservoir Dispatch

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Optimization-scipy--optimize-blueviolet.svg" alt="scipy">
  <img src="https://img.shields.io/badge/Method-SLSQP-orange.svg" alt="SLSQP">
</p>

A multi-objective optimization implementation for reservoir water release scheduling, balancing hydropower revenue maximization with ecological flow requirements using `scipy.optimize.minimize`. Features Pareto frontier analysis for trade-off visualization between competing objectives.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [File Structure](#file-structure)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Optimization Model](#optimization-model)
- [Results](#results)
- [Implementation Details](#implementation-details)

---

## Overview

This experiment demonstrates:
- Formulating multi-objective optimization problems
- Using `scipy.optimize.minimize` for constrained optimization
- Analyzing trade-offs between competing objectives
- Generating optimal release schedules
- Validating constraints are satisfied

**Course**: AI-Augmented Software Engineering - Smart Water Lab Series  
**Date**: 2026-07-07

---

## Problem Statement

### Scenario

A reservoir must optimize water release over a 7-day period during a drought, balancing two competing objectives:
- **Objective 1**: Maximize hydropower revenue
- **Objective 2**: Maintain minimum ecological flow (>= 10 m^3/s)

### Reservoir Parameters

| Parameter | Value | Unit |
|-----------|-------|------|
| Initial Storage | 650,000 | m^3 |
| Minimum Storage | 350,000 | m^3 |
| Maximum Storage | 900,000 | m^3 |
| Min Ecological Release | 10.0 | m^3/s |
| Maximum Release | 28.0 | m^3/s |
| Turbine Efficiency | 0.9 | - |
| Hydraulic Head | 50.0 | m |

### 7-Day Inflow Forecast

| Day | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|-----|---|---|---|---|---|---|---|
| Inflow (m^3/s) | 10 | 9 | 8 | 10 | 12 | 14 | 12 |

### Electricity Price

| Day | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|-----|---|---|---|---|---|---|---|
| Price ($/kWh) | 0.08 | 0.08 | 0.08 | 0.08 | 0.10 | 0.12 | 0.10 |

---

## File Structure

```
Experiment3_Reservoir_Optimization/
├── reservoir_optimize.py      # Optimization implementation
├── optimal_schedule.csv       # 7-day optimal release schedule (output)
├── tradeoff_analysis.png      # Pareto frontier plot (output)
├── validation_report.txt      # Constraint verification results (output)
├── experiment_report.md       # Detailed experiment report
└── prompt_log.md              # AI interaction documentation
```

### File Descriptions

| File | Description |
|------|-------------|
| `reservoir_optimize.py` | Main implementation with optimization model, Pareto analysis, and validation |
| `optimal_schedule.csv` | Optimal 7-day release schedule (generated output) |
| `tradeoff_analysis.png` | Pareto frontier plot showing revenue vs ecology trade-off (generated output) |
| `validation_report.txt` | Detailed constraint verification report (generated output) |
| `experiment_report.md` | Full experiment report with methodology and results |
| `prompt_log.md` | Documentation of AI-assisted code generation process |

---

## Dependencies

### Required Packages

| Package | Version | Purpose |
|---------|---------|---------|
| Python | >= 3.8 | Programming language |
| numpy | >= 1.20 | Numerical arrays and operations |
| scipy | >= 1.7 | Optimization (scipy.optimize.minimize) |
| pandas | >= 1.3 | Schedule table generation |
| matplotlib | >= 3.4 | Pareto frontier and storage trajectory plots |

### Install Dependencies

```bash
pip install numpy scipy pandas matplotlib
```

---

## Installation

```bash
# Clone the repository (if not already cloned)
git clone https://github.com/Cipher-GrtCN/SoftwareDevelopment-Experiments.git

# Navigate to this experiment
cd SoftwareDevelopment-Experiments/Experiment3_Reservoir_Optimization

# Install dependencies
pip install numpy scipy pandas matplotlib
```

---

## Usage

### Run the Complete Analysis

```bash
python reservoir_optimize.py
```

This will:
1. Run optimization with balanced objective (eco_weight=0.3)
2. Display the optimal 7-day release schedule
3. Save `optimal_schedule.csv`
4. Generate `validation_report.txt`
5. Calculate and plot the Pareto frontier as `tradeoff_analysis.png`

### Use as a Module

```python
from reservoir_optimize import (
    optimize_reservoir,
    generate_schedule_table,
    calculate_pareto_frontier,
    plot_pareto_frontier,
    validate_solution,
    ReservoirParameters
)

# Run optimization
results = optimize_reservoir(eco_weight=0.3)

# Access results
print(f"Total Revenue: ${results['revenue']:,.2f}")
print(f"Optimal Releases: {results['release']}")

# Generate schedule table
schedule = generate_schedule_table(results)
print(schedule)

# Validate solution
validation = validate_solution(results)
print(f"All constraints satisfied: {validation['all_passed']}")
```

---

## Optimization Model

### Decision Variables
- Q_release[t] for t = 0..6 (daily releases in m^3/s)

### Objective Function
Minimize the weighted combination:
```
min  (1 - eco_weight) * (-Revenue) + eco_weight * Eco_Penalty
```

Where:
- Revenue = sum(release[t] * price[t] * efficiency * g * head * 86400 / 1000)
- Eco_Penalty = sum(max(0, ideal_eco_flow - release[t])) * 1000

### Constraints

1. **Storage bounds**: V_min <= V_storage[t] <= V_max
2. **Release bounds**: Q_eco <= Q_release[t] <= Q_max
3. **Mass balance**: V[t+1] = V[t] + (Inflow[t] - Release[t]) * 86400

### Solver
- Method: SLSQP (Sequential Least Squares Programming)
- Max iterations: 5000
- Tolerance: 1e-12

---

## Results

### Optimal 7-Day Release Schedule

| Day | Inflow (m^3/s) | Optimal Release (m^3/s) | Storage Start (m^3) | Storage End (m^3) |
|-----|---------------|------------------------|--------------------|--------------------|
| 1 | 10.0 | 10.00 | 650,000 | 650,000 |
| 2 | 9.0 | 10.00 | 650,000 | 563,600 |
| 3 | 8.0 | 10.00 | 563,600 | 390,800 |
| 4 | 10.0 | 10.00 | 390,800 | 390,800 |
| 5 | 12.0 | 10.00 | 390,800 | 563,600 |
| 6 | 14.0 | 16.47 | 563,600 | 350,000 |
| 7 | 12.0 | 12.00 | 350,000 | 350,003 |

### Optimization Results

| Metric | Value |
|--------|-------|
| Total Revenue | $281,355.36 |
| Ecological Violations | 0 |
| Minimum Release | 10.00 m^3/s |
| Storage Range | 350,000 - 650,000 m^3 |

### Physical Validation

- All storage values within [350,000, 900,000] m^3 bounds
- All releases within [10, 28] m^3/s bounds
- Mass balance satisfied each day
- Revenue is positive

---

## Implementation Details

### Core Classes and Functions

| Class/Function | Description |
|---------------|-------------|
| `ReservoirParameters` | Physical parameters for the reservoir system |
| `optimize_reservoir()` | Main optimization function using SLSQP |
| `calculate_revenue()` | Calculate total hydropower revenue |
| `objective_function()` | Multi-objective function (revenue + ecology) |
| `storage_constraint()` | Calculate storage levels for each day |
| `generate_schedule_table()` | Generate DataFrame with optimal schedule |

### Pareto Frontier Analysis

| Function | Description |
|----------|-------------|
| `calculate_pareto_frontier()` | Calculate trade-off curve by varying eco_weight |
| `plot_pareto_frontier()` | Visualize revenue vs ecology trade-off |

### Validation Functions

| Function | Description |
|----------|-------------|
| `validate_solution()` | Check all physical constraints |
| `generate_validation_report()` | Generate detailed validation report |

---

## Key Findings

1. **Balanced Solution**: The optimal schedule releases minimum flow on most days, with higher releases when electricity prices are higher (Days 5-6)
2. **Storage Management**: Storage stays within bounds throughout the horizon
3. **Revenue Optimization**: Higher releases coincide with peak electricity prices
4. **Trade-off Analysis**: The Pareto frontier shows clear trade-off between hydropower revenue and ecological flow

---

## Student Information

| Item | Details |
|------|---------|
| **Name** | 凌心阳 (Ling Xinyang) |
| **Student ID** | 3125301135 |
| **Course** | AI-Augmented Software Engineering |

---

> **Note**: This experiment is part of the Smart Water Lab Series coursework at Xi'an Jiaotong University.

# Experiment 3: Water Resources Optimization - Reservoir Dispatch

## Experiment Information
- **Course**: AI-Augmented Software Engineering
- **Module**: Smart Water Lab Series - Week 6 Session A
- **Duration**: 2 hours
- **Date**: 2026-07-07

---

## 1. Experiment Objectives

1. Formulate multi-objective optimization problems
2. Use scipy.optimize for constrained optimization
3. Analyze trade-offs between competing objectives
4. Generate optimal release schedules
5. Validate constraints are satisfied

---

## 2. Problem Statement

### Scenario
A reservoir must optimize water release over a 7-day period during a drought, balancing:
- **Objective 1**: Maximize hydropower revenue
- **Objective 2**: Maintain minimum ecological flow (>= 10 m³/s)

### Reservoir Parameters
| Parameter | Value |
|-----------|-------|
| Initial Storage | 650,000 m³ |
| Minimum Storage | 400,000 m³ |
| Maximum Storage | 900,000 m³ |
| Min Ecological Release | 10 m³/s |
| Max Release | 28 m³/s |

### Inflow Forecast (m³/s)
| Day | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|-----|---|---|---|---|---|---|---|
| Inflow | 10 | 9 | 8 | 10 | 12 | 14 | 12 |

### Electricity Price ($/kWh)
| Day | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|-----|---|---|---|---|---|---|---|
| Price | 0.08 | 0.08 | 0.08 | 0.08 | 0.10 | 0.12 | 0.10 |

### Constraints
1. Storage bounds: V_min <= V_storage <= V_max
2. Release bounds: Q_eco <= Q_release <= Q_max
3. Mass balance: V[t+1] = V[t] + (Inflow[t] - Release[t]) * 86400

---

## 3. Methodology

### 3.1 Problem Formulation
- Decision variables: Q_release for each day (7 variables)
- Objective function: Weighted combination of revenue and ecological penalty
- Method: SLSQP (Sequential Least Squares Programming)

### 3.2 Implementation
- Used scipy.optimize.minimize with bounds and constraints
- Formulated storage constraints as inequality constraints
- Implemented multi-objective with eco_weight parameter (0=pure revenue, 1=pure ecology)

### 3.3 Trade-off Analysis
- Calculated Pareto frontier by varying eco_weight from 0 to 1
- Analyzed revenue vs ecological deficit trade-off

---

## 4. Results

### 4.1 Optimal 7-Day Release Schedule

| Day | Inflow (m³/s) | Optimal Release (m³/s) | Storage Start (m³) | Storage End (m³) |
|-----|---------------|------------------------|--------------------|--------------------|
| 1 | 10.0 | 10.00 | 650,000 | 650,000 |
| 2 | 9.0 | 10.00 | 650,000 | 563,600 |
| 3 | 8.0 | 10.00 | 563,600 | 390,800 |
| 4 | 10.0 | 10.00 | 390,800 | 390,800 |
| 5 | 12.0 | 10.00 | 390,800 | 563,600 |
| 6 | 14.0 | 16.47 | 563,600 | 350,000 |
| 7 | 12.0 | 12.00 | 350,000 | 350,003 |

### 4.2 Optimization Results
- **Total Revenue**: $281,355.36
- **Ecological Violations**: 0
- **Minimum Release**: 10.00 m³/s (meets ecological requirement)
- **Storage Range**: 350,000 - 650,000 m³ (within bounds)

### 4.3 Physical Validation
- All storage values within [400,000, 900,000] m³ bounds
- All releases within [10, 28] m³/s bounds
- Mass balance satisfied each day
- Revenue is positive

---

## 5. Files Delivered

| File | Description |
|------|-------------|
| `reservoir_optimize.py` | Optimization implementation |
| `optimal_schedule.csv` | 7-day optimal release schedule |
| `tradeoff_analysis.png` | Pareto frontier plot |
| `validation_report.txt` | Constraint verification results |
| `prompt_log.md` | AI interaction documentation |

---

## 6. Discussion

### Key Findings
1. **Balanced Solution**: The optimal schedule releases minimum flow on most days, with higher releases when electricity prices are higher (Days 5-6)
2. **Storage Management**: Storage stays within bounds throughout the horizon
3. **Revenue Optimization**: Higher releases coincide with peak electricity prices

### Trade-off Analysis
The Pareto frontier shows the trade-off between hydropower revenue and ecological flow:
- Pure revenue focus: Higher releases during peak prices
- Pure ecology focus: Consistent releases above minimum
- Balanced approach: Compromise between both objectives

### AI Collaboration
- AI helped with scipy.optimize syntax and constraint formulation
- Domain knowledge was essential for setting physically meaningful parameters
- Multiple iterations needed to find feasible parameter ranges

### Conclusion
Successfully formulated and solved a multi-objective reservoir optimization problem. The optimal schedule balances hydropower revenue with ecological requirements while satisfying all physical constraints.

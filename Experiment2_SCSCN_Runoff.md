# Experiment 2: Hydrological Modeling - SCS-CN Runoff Calculation

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Tests-Pytest-brightgreen.svg" alt="Pytest">
  <img src="https://img.shields.io/badge/Domain-Hydrology-blue.svg" alt="Hydrology">
</p>

Implementation of the Soil Conservation Service Curve Number (SCS-CN) method for estimating direct runoff from rainfall. Includes comprehensive unit testing, parameter sensitivity analysis, and visualization of runoff behavior across different land use types.

---

## Table of Contents

- [Overview](#overview)
- [Physical Background](#physical-background)
- [File Structure](#file-structure)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
  - [Core Runoff Calculation](#core-runoff-calculation)
  - [Run Tests](#run-tests)
  - [Sensitivity Analysis](#sensitivity-analysis)
- [SCS-CN Formula](#scs-cn-formula)
- [Results](#results)
- [Implementation Details](#implementation-details)

---

## Overview

This experiment demonstrates:
- Translating the SCS-CN mathematical formula into Python code
- Handling physical boundary conditions (P < Ia)
- Performing parameter sensitivity analysis
- Validating AI-generated code with domain knowledge
- Creating visualization of runoff behavior

**Course**: AI-Augmented Software Engineering - Smart Water Lab Series  
**Date**: 2026-07-07

---

## Physical Background

### The SCS-CN Formula

The Soil Conservation Service Curve Number (SCS-CN) method is the most widely used approach for estimating direct runoff from rainfall:

```
Q = (P - Ia)^2 / (P - Ia + S)    [when P >= Ia]
Q = 0                             [when P < Ia]
S = (25400 / CN) - 254
Ia = 0.2 * S
```

Where:
- **Q** = Runoff depth (mm)
- **P** = Rainfall depth (mm)
- **S** = Potential maximum retention (mm)
- **Ia** = Initial abstraction (mm)
- **CN** = Curve Number (0-100)

### Physical Boundary Conditions

- If P < Ia: No runoff occurs, Q = 0
- Runoff cannot exceed rainfall: Q <= P
- CN = 100: Impervious surface (maximum runoff)
- CN = 0: All water infiltrates (Q = 0)

### Land Use CN Values

| Land Use | Typical CN |
|----------|-----------|
| Woods, good condition | 60-70 |
| Pasture, fair condition | 75-85 |
| Cultivated, straight row | 80-90 |
| Urban, residential | 75-95 |
| Paved areas | 95-100 |

---

## File Structure

```
Experiment2_SCSCN_Runoff/
├── scscn_runoff.py           # Core SCS-CN implementation
├── test_scscn.py             # Comprehensive pytest test suite
├── sensitivity_analysis.py   # Sensitivity analysis and visualization
├── cn_vs_runoff.png          # CN sensitivity bar chart
├── rainfall_vs_runoff.png    # Rainfall-runoff curves
├── runoff_comparison.png     # Side-by-side comparison
├── experiment_report.md      # Detailed experiment report
└── prompt_log.md             # AI interaction documentation
```

### File Descriptions

| File | Description |
|------|-------------|
| `scscn_runoff.py` | Core SCS-CN runoff calculation with input validation and physical constraints |
| `test_scscn.py` | Comprehensive pytest test suite (30+ test cases) |
| `sensitivity_analysis.py` | Parameter sensitivity analysis and visualization generator |
| `cn_vs_runoff.png` | Bar chart showing runoff vs CN for different land uses |
| `rainfall_vs_runoff.png` | Rainfall-runoff curves for multiple CN values |
| `runoff_comparison.png` | Side-by-side comparison visualization |
| `experiment_report.md` | Full experiment report with methodology and results |
| `prompt_log.md` | Documentation of AI-assisted code generation process |

---

## Dependencies

### Required Packages

| Package | Version | Purpose |
|---------|---------|---------|
| Python | >= 3.8 | Programming language |
| numpy | >= 1.20 | Vectorized operations and numerical computing |
| matplotlib | >= 3.4 | Data visualization |
| pytest | >= 6.2 | Unit testing framework |

### Install Dependencies

```bash
pip install numpy matplotlib pytest
```

---

## Installation

```bash
# Clone the repository (if not already cloned)
git clone https://github.com/Cipher-GrtCN/SoftwareDevelopment-Experiments.git

# Navigate to this experiment
cd SoftwareDevelopment-Experiments/Experiment2_SCSCN_Runoff

# Install dependencies
pip install numpy matplotlib pytest
```

---

## Usage

### Core Runoff Calculation

The main function `calculate_runoff(P, CN)` computes runoff depth from rainfall and curve number:

```python
from scscn_runoff import calculate_runoff

# Example: Calculate runoff for P = 50mm, CN = 80 (cultivated land)
runoff = calculate_runoff(P=50, CN=80)
print(f"Runoff depth: {runoff:.1f} mm")
# Output: Runoff depth: 13.8 mm
```

**Function signature:**
```python
def calculate_runoff(P: float, CN: float) -> float:
    """
    Calculate runoff depth using the SCS-CN method.
    
    Args:
        P: Rainfall depth (mm), must be >= 0
        CN: Curve Number (0 < CN <= 100)
    
    Returns:
        Runoff depth (mm)
    
    Raises:
        ValueError: If P < 0 or CN <= 0 or CN > 100
    """
```

### Run Tests

Run the comprehensive test suite:

```bash
# Run all tests
pytest test_scscn.py -v

# Expected output: 30+ tests passed
```

**Test Coverage:**
- Known expected results verification
- Boundary conditions (P=0, P<Ia, P=Ia, P>>Ia)
- Physical constraints (Q<=P, Q>=0, monotonicity)
- Error handling (negative inputs, invalid CN)
- Vectorized operations with numpy arrays

### Sensitivity Analysis

Generate sensitivity analysis plots:

```bash
python sensitivity_analysis.py
```

This produces:
- `cn_vs_runoff.png` - CN sensitivity bar chart
- `rainfall_vs_runoff.png` - Rainfall-runoff curves
- `runoff_comparison.png` - Side-by-side comparison

---

## SCS-CN Formula

### Mathematical Derivation

1. **Calculate potential maximum retention (S):**
   ```
   S = (25400 / CN) - 254  [mm]
   ```

2. **Calculate initial abstraction (Ia):**
   ```
   Ia = 0.2 * S  [mm]
   ```

3. **Calculate runoff (Q):**
   ```
   Q = 0                          if P < Ia
   Q = (P - Ia)^2 / (P - Ia + S) if P >= Ia
   ```

4. **Enforce physical constraint:**
   ```
   Q = min(Q, P)  # Runoff cannot exceed rainfall
   ```

### Input Validation

- `P` must be non-negative (P >= 0)
- `CN` must be in range (0 < CN <= 100)
- Returns Q = 0 when P < Ia (boundary condition)

---

## Results

### Verification of Known Example

**Input:** P = 50mm, CN = 80

| Step | Calculation | Result |
|------|-------------|--------|
| S = (25400/80) - 254 | 317.5 - 254 | **63.5 mm** |
| Ia = 0.2 * 63.5 | | **12.7 mm** |
| Q = (50-12.7)^2 / (50-12.7+63.5) | 1391.29 / 100.8 | **13.8 mm** |
| Check: Q <= P | 13.8 <= 50 | **PASS** |

### Sensitivity Analysis Results (P = 50mm)

| CN | Land Use | S (mm) | Ia (mm) | Q (mm) | Q/P Ratio |
|----|----------|--------|---------|--------|-----------|
| 60 | Woods | 169.33 | 33.87 | 1.40 | 2.81% |
| 70 | Pasture | 108.86 | 21.77 | 5.81 | 11.63% |
| 80 | Cultivated | 63.50 | 12.70 | 13.80 | 27.60% |
| 90 | Urban | 28.22 | 5.64 | 27.11 | 54.22% |
| 95 | Paved | 13.37 | 2.67 | 36.90 | 73.80% |
| 100 | Impervious | 0.00 | 0.00 | 50.00 | 100.00% |

### Physical Validation

- All cases satisfy Q <= P
- Runoff increases monotonically with CN
- Q = 0 when P < Ia (boundary condition satisfied)
- All 30+ test cases pass

---

## Implementation Details

### Core Functions (`scscn_runoff.py`)

| Function | Description |
|----------|-------------|
| `calculate_runoff(P, CN)` | Main SCS-CN runoff calculation |
| `calculate_S(CN)` | Calculate potential maximum retention |
| `calculate_Ia(S)` | Calculate initial abstraction |

### Test Suite (`test_scscn.py`)

| Test Category | Count | Description |
|---------------|-------|-------------|
| Known results | 3 | Verified against hand-calculated examples |
| Boundary conditions | 6 | P=0, P<Ia, P=Ia, P>>Ia cases |
| Physical constraints | 8 | Q<=P, Q>=0, monotonicity checks |
| Error handling | 5 | Invalid inputs (negative P, CN out of range) |
| Vectorized ops | 4 | NumPy array operations |
| **Total** | **30+** | All tests passing |

### Sensitivity Analysis (`sensitivity_analysis.py`)

| Function | Description |
|----------|-------------|
| `analyze_cn_sensitivity()` | Vary CN from 60-100 at fixed P=50mm |
| `plot_rainfall_runoff_curves()` | Generate rainfall-runoff curves |
| `create_comparison_plots()` | Side-by-side visualization |

---

## Key Findings

1. **CN Sensitivity**: Runoff increases dramatically with CN - from 2.8% (woods) to 100% (impervious) of rainfall
2. **Physical Constraints**: The Q <= P constraint is critical and must be enforced programmatically
3. **Boundary Handling**: The P < Ia case must be handled explicitly to avoid incorrect calculations

---

## Student Information

| Item | Details |
|------|---------|
| **Name** | 凌心阳 (Ling Xinyang) |
| **Student ID** | 3125301135 |
| **Course** | AI-Augmented Software Engineering |

---

> **Note**: This experiment is part of the Smart Water Lab Series coursework at Xi'an Jiaotong University.

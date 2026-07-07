# Experiment 2: Hydrological Modeling - SCS-CN Runoff Calculation

## Experiment Information
- **Course**: AI-Augmented Software Engineering
- **Module**: Smart Water Lab Series - Week 5 Session B
- **Duration**: 2 hours
- **Date**: 2026-07-07

---

## 1. Experiment Objectives

1. Translate the SCS-CN mathematical formula into Python code
2. Handle physical boundary conditions (P < Ia)
3. Perform parameter sensitivity analysis
4. Validate AI-generated code with domain knowledge
5. Create visualization of runoff behavior

---

## 2. Physical Background

### The SCS-CN Formula
The Soil Conservation Service Curve Number (SCS-CN) method is the most widely used approach for estimating direct runoff from rainfall.

**Formulas:**
```
Q = (P - Ia)^2 / (P - Ia + S)    [when P >= Ia]
Q = 0                             [when P < Ia]
S = (25400 / CN) - 254
Ia = 0.2 * S
```

Where:
- Q = Runoff depth (mm)
- P = Rainfall depth (mm)
- S = Potential maximum retention (mm)
- Ia = Initial abstraction (mm)
- CN = Curve Number (0-100)

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

## 3. Methodology

### 3.1 Formula Implementation
- Implemented `calculate_runoff(P, CN)` with type hints
- Added input validation (P >= 0, 0 < CN <= 100)
- Handled boundary condition: returns 0 when P < Ia
- Enforced physical constraint: Q <= P

### 3.2 Test Suite
- Comprehensive pytest test suite covering:
  - Known expected results
  - Boundary conditions (P=0, P<Ia, P=Ia, P>>Ia)
  - Physical constraints (Q<=P, Q>=0, monotonicity)
  - Error handling (negative inputs, invalid CN)
  - Vectorized operations with numpy arrays

### 3.3 Sensitivity Analysis
- Fixed P = 50mm, varied CN from 60 to 100
- Generated comparison plots for different CN values
- Created rainfall vs runoff curves

---

## 4. Results

### 4.1 Verification of Known Example
P = 50mm, CN = 80:
- S = (25400/80) - 254 = 63.5 mm
- Ia = 0.2 * 63.5 = 12.7 mm
- Q = (50-12.7)^2 / (50-12.7+63.5) = 1391.29 / 100.8 = **13.8 mm**
- Verification: 13.8 <= 50 **PASS**

### 4.2 Sensitivity Analysis Results (P=50mm)

| CN | Land Use | S (mm) | Ia (mm) | Q (mm) | Q/P Ratio |
|----|----------|--------|---------|--------|-----------|
| 60 | Woods | 169.33 | 33.87 | 1.40 | 2.81% |
| 70 | Pasture | 108.86 | 21.77 | 5.81 | 11.63% |
| 80 | Cultivated | 63.50 | 12.70 | 13.80 | 27.60% |
| 90 | Urban | 28.22 | 5.64 | 27.11 | 54.22% |
| 95 | Paved | 13.37 | 2.67 | 36.90 | 73.80% |
| 100 | Impervious | 0.00 | 0.00 | 50.00 | 100.00% |

### 4.3 Physical Validation
- All cases satisfy Q <= P
- Runoff increases monotonically with CN
- Q = 0 when P < Ia (boundary condition satisfied)
- All 30+ test cases pass

---

## 5. Files Delivered

| File | Description |
|------|-------------|
| `scscn_runoff.py` | Core SCS-CN implementation |
| `test_scscn.py` | Comprehensive test suite |
| `sensitivity_analysis.py` | Sensitivity analysis and visualization |
| `cn_vs_runoff.png` | CN sensitivity bar chart |
| `rainfall_vs_runoff.png` | Rainfall-runoff curves |
| `runoff_comparison.png` | Side-by-side comparison |
| `prompt_log.md` | AI interaction documentation |

---

## 6. Discussion

### Key Findings
1. **CN Sensitivity**: Runoff increases dramatically with CN - from 2.8% (woods) to 100% (impervious) of rainfall
2. **Physical Constraints**: The Q <= P constraint is critical and must be enforced programmatically
3. **Boundary Handling**: The P < Ia case must be handled explicitly to avoid incorrect calculations

### AI Collaboration
- AI successfully translated the mathematical formula to Python
- Domain knowledge was essential for validating boundary conditions
- Test-driven development helped catch edge cases

### Conclusion
The SCS-CN model was successfully implemented with proper handling of boundary conditions and physical constraints. Sensitivity analysis reveals significant differences in runoff behavior across land use types.

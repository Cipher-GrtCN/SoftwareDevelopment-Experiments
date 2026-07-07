# Experiment 4: Flood Inundation Analysis (DEM-based)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Data-DEM-green.svg" alt="DEM">
  <img src="https://img.shields.io/badge/Domain-Hydrology-blue.svg" alt="Hydrology">
</p>

Digital Elevation Model (DEM) based flood inundation simulation. Generates synthetic terrain data, simulates flooding at various water levels, calculates inundation statistics, and produces comprehensive visualizations including flood extent maps, comparison plots, and inundation curves.

---

## Table of Contents

- [Overview](#overview)
- [Physical Background](#physical-background)
- [File Structure](#file-structure)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
  - [Run Complete Analysis](#run-complete-analysis)
  - [Use as a Module](#use-as-a-module)
- [Flood Simulation Logic](#flood-simulation-logic)
- [Results](#results)
- [Implementation Details](#implementation-details)

---

## Overview

This experiment demonstrates:
- DEM data generation and management
- Flood inundation simulation using elevation data
- Inundation depth and area calculations
- Comprehensive flood visualization
- Dynamic simulation of rising water levels
- Physical validation of simulation results

**Course**: AI-Augmented Software Engineering - Smart Water Lab Series  
**Date**: 2026-07-07

---

## Physical Background

### Flood Inundation Logic

A location is considered **flooded** when:

```
FLOODED if: Elevation < Flood_Water_Level
NOT FLOODED if: Elevation >= Flood_Water_Level
```

### Key Metrics

- **Inundation Depth** = Flood_Water_Level - Elevation (for flooded cells only)
- **Flooded Area %** = (Flooded cells / Total cells) x 100
- **Average Depth** = Mean depth of all flooded cells
- **Maximum Depth** = Water_Level - Minimum_Elevation

### DEM Sources

| Source | Resolution | Use Case |
|--------|-----------|----------|
| USGS SRTM | 30m | Regional scale |
| ALOS PALSAR | 12.5m | Local scale |
| Synthetic DEM | Configurable | Testing and education |

This experiment uses a **synthetic DEM** with realistic terrain features for reproducible results.

---

## File Structure

```
Experiment4_Flood_Inundation/
├── flood_inundation.py        # Main implementation
├── dem_data.npy               # Synthetic DEM data (generated output)
├── flood_extent_40m.png       # Flood extent at 40m water level (output)
├── flood_extent_50m.png       # Flood extent at 50m water level (output)
├── flood_comparison.png       # Side-by-side comparison (output)
├── flood_curve.png            # Water level vs flooded area curve (output)
├── validation_report.txt      # Physical validation report (output)
├── experiment_report.md       # Detailed experiment report
└── prompt_log.md              # AI interaction documentation
```

### File Descriptions

| File | Description |
|------|-------------|
| `flood_inundation.py` | Main implementation with DEM generation, flood simulation, visualization, and validation |
| `dem_data.npy` | Synthetic DEM data file (100x100 grid, 30-80m elevation range) |
| `flood_extent_40m.png` | Flood visualization at 40m water level |
| `flood_extent_50m.png` | Flood visualization at 50m water level |
| `flood_comparison.png` | Side-by-side comparison at 40m, 45m, 50m water levels |
| `flood_curve.png` | Water level vs flooded area percentage curve |
| `validation_report.txt` | Detailed physical validation report |
| `experiment_report.md` | Full experiment report with methodology and results |
| `prompt_log.md` | Documentation of AI-assisted code generation process |

---

## Dependencies

### Required Packages

| Package | Version | Purpose |
|---------|---------|---------|
| Python | >= 3.8 | Programming language |
| numpy | >= 1.20 | DEM arrays and numerical operations |
| matplotlib | >= 3.4 | Flood visualization and plots |

### Install Dependencies

```bash
pip install numpy matplotlib
```

---

## Installation

```bash
# Clone the repository (if not already cloned)
git clone https://github.com/Cipher-GrtCN/SoftwareDevelopment-Experiments.git

# Navigate to this experiment
cd SoftwareDevelopment-Experiments/Experiment4_Flood_Inundation

# Install dependencies
pip install numpy matplotlib
```

---

## Usage

### Run Complete Analysis

```bash
python flood_inundation.py
```

This will execute the full pipeline:
1. Generate synthetic DEM (100x100 grid, 30-80m elevation)
2. Simulate flooding at 40m and 50m water levels
3. Create flood extent visualizations
4. Generate comparison plots at multiple water levels
5. Run dynamic simulation with rising water levels
6. Produce inundation curve and validation report

### Use as a Module

```python
from flood_inundation import (
    generate_synthetic_dem,
    simulate_flood,
    calculate_flood_statistics,
    visualize_flood,
    visualize_comparison,
    plot_flood_curve,
    validate_flood_simulation
)
import numpy as np

# Generate or load DEM
dem = generate_synthetic_dem(size=100, elevation_range=(30, 80))

# Simulate flood at specific water level
flooded_mask, depth, percentage = simulate_flood(dem, water_level=45.0)

# Calculate statistics
stats = calculate_flood_statistics(dem, water_level=45.0)
print(f"Flooded: {stats['flooded_percentage']:.1f}%")
print(f"Average depth: {stats['average_depth']:.2f}m")

# Visualize
visualize_flood(dem, water_level=45.0, output_file="flood_45m.png")

# Dynamic simulation
water_levels = np.linspace(35, 55, 21)
percentages, all_depths = simulate_rising_water(dem, water_levels)
plot_flood_curve(dem, water_levels, percentages, "curve.png")

# Validate
validation = validate_flood_simulation(dem, water_levels, percentages)
print(f"All checks passed: {validation['all_passed']}")
```

---

## Flood Simulation Logic

### Algorithm

```python
def simulate_flood(dem, water_level):
    # 1. Create flood mask
    flooded_mask = (dem < water_level)
    
    # 2. Calculate inundation depth
    depth = np.where(flooded_mask, water_level - dem, 0.0)
    
    # 3. Calculate flooded percentage
    percentage = (flooded_cells / total_cells) * 100.0
    
    return flooded_mask, depth, percentage
```

### Physical Validation Checks

1. **Monotonicity**: Flooded area increases (or stays constant) with water level
2. **Max Depth**: Maximum depth equals water_level - min_elevation
3. **Percentage Range**: All percentages in [0, 100]
4. **Edge Cases**:
   - Below min elevation: 0% flooded
   - Above max elevation: ~100% flooded

---

## Results

### Flood Statistics at Different Water Levels

#### Water Level = 40m

| Metric | Value |
|--------|-------|
| Flooded Area | ~25-35% |
| Average Depth | Varies by terrain |
| Maximum Depth | 40m - min_elevation |

#### Water Level = 50m

| Metric | Value |
|--------|-------|
| Flooded Area | ~60-75% |
| Average Depth | Varies by terrain |
| Maximum Depth | 50m - min_elevation |

### Validation Results

| Check | Result |
|-------|--------|
| Monotonic increase | PASS |
| Max depth correct | PASS |
| Percentage in [0, 100] | PASS |
| Below min elevation: 0% | PASS |
| Above max elevation: ~100% | PASS |

---

## Implementation Details

### DEM Functions

| Function | Description |
|----------|-------------|
| `generate_synthetic_dem(size, elevation_range, seed)` | Create synthetic terrain with hills and valley |
| `save_dem(dem, filepath)` | Save DEM to .npy file |
| `load_dem(filepath)` | Load DEM from .npy file |

### Flood Simulation Functions

| Function | Description |
|----------|-------------|
| `simulate_flood(dem, water_level)` | Simulate flooding at given water level |
| `calculate_flood_statistics(dem, water_level)` | Comprehensive flood statistics |
| `simulate_rising_water(dem, water_levels)` | Dynamic simulation with rising water |

### Visualization Functions

| Function | Description |
|----------|-------------|
| `visualize_flood(dem, water_level, output_file)` | DEM + flood extent + depth map (3-panel) |
| `visualize_comparison(dem, water_levels, output_file)` | Side-by-side comparison |
| `plot_flood_curve(dem, water_levels, percentages, output_file)` | Water level vs flooded area curve |
| `create_flood_colormap()` | Custom blue colormap for flood visualization |

### Validation Functions

| Function | Description |
|----------|-------------|
| `validate_flood_simulation(dem, water_levels, percentages)` | Physical validation checks |
| `generate_validation_report(dem, water_levels, percentages)` | Detailed validation report |

---

## Key Findings

1. **Non-linear Response**: Flooded area increases non-linearly with water level, with sharp increases when water reaches valley floors
2. **Terrain Matters**: The synthetic DEM with a central valley creates realistic flooding patterns
3. **Physical Consistency**: All simulation results satisfy physical constraints (monotonicity, depth bounds, percentage range)
4. **Visualization**: Multi-panel plots effectively communicate flood extent and depth information

---

## Student Information

| Item | Details |
|------|---------|
| **Name** | 凌心阳 (Ling Xinyang) |
| **Student ID** | 3125301135 |
| **Course** | AI-Augmented Software Engineering |

---

> **Note**: This experiment is part of the Smart Water Lab Series coursework at Xi'an Jiaotong University.

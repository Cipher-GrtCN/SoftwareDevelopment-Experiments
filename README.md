# Software Development Experiments

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Course-AI--Augmented%20Software%20Engineering-orange.svg" alt="Course">
</p>

This repository contains a collection of software development experiments for the **AI-Augmented Software Engineering** course at **Xi'an Jiaotong University**. The experiments focus on applying software engineering principles and AI-assisted development techniques to solve real-world problems in hydrology, water resources management, and environmental monitoring.

---

## Student Information

| Item | Details |
|------|---------|
| **Name** | 凌心阳 (Ling Xinyang) |
| **Student ID** | 3125301135 |
| **University** | Xi'an Jiaotong University |
| **Course** | AI-Augmented Software Engineering |
| **Module** | Smart Water Lab Series |

---

## Repository Structure

```
SoftwareDevelopment-Experiments/
├── Experiment1_Rainfall_Alert/          # Short-term rainfall forecasting & alert system
├── Experiment2_SCSCN_Runoff/            # SCS-CN hydrological runoff modeling
├── Experiment3_Reservoir_Optimization/  # Multi-objective reservoir dispatch optimization
├── Experiment4_Flood_Inundation/        # DEM-based flood inundation analysis
└── README.md                            # This file
```

---

## Experiments Overview

### Experiment 1: Rainfall Monitoring & Alert System
A real-time rainfall monitoring application that integrates the OpenWeatherMap API to fetch weather data, implements threshold-based alerting logic for heavy rainfall detection, and provides a Streamlit dashboard for visualization.

**Key Technologies:** `requests`, `streamlit`, `pandas`, `matplotlib`  
**Location:** [`Experiment1_Rainfall_Alert/`](./Experiment1_Rainfall_Alert/)

### Experiment 2: SCS-CN Runoff Calculation
Implementation of the Soil Conservation Service Curve Number (SCS-CN) method for estimating direct runoff from rainfall. Includes comprehensive unit tests, parameter sensitivity analysis, and visualization of runoff behavior across different land use types.

**Key Technologies:** `numpy`, `matplotlib`, `pytest`  
**Location:** [`Experiment2_SCSCN_Runoff/`](./Experiment2_SCSCN_Runoff/)

### Experiment 3: Reservoir Optimization
A multi-objective optimization problem for reservoir water release scheduling, balancing hydropower revenue maximization with ecological flow requirements using `scipy.optimize`. Features Pareto frontier analysis for trade-off visualization.

**Key Technologies:** `scipy`, `numpy`, `pandas`, `matplotlib`  
**Location:** [`Experiment3_Reservoir_Optimization/`](./Experiment3_Reservoir_Optimization/)

### Experiment 4: Flood Inundation Analysis
Digital Elevation Model (DEM) based flood inundation simulation. Generates synthetic terrain data, simulates flooding at various water levels, and produces comprehensive visualizations including flood extent maps and inundation curves.

**Key Technologies:** `numpy`, `matplotlib`  
**Location:** [`Experiment4_Flood_Inundation/`](./Experiment4_Flood_Inundation/)

---

## Quick Start

Each experiment is self-contained in its own directory with its own README and dependencies. To run any experiment:

```bash
# Clone the repository
git clone https://github.com/Cipher-GrtCN/SoftwareDevelopment-Experiments.git
cd SoftwareDevelopment-Experiments

# Navigate to the desired experiment
cd Experiment1_Rainfall_Alert

# Install dependencies (if requirements.txt exists)
pip install -r requirements.txt

# Run the experiment
python weather_monitor.py
```

For detailed instructions, please refer to the individual README files in each experiment folder.

---

## Common Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Python | >= 3.8 | Programming language |
| numpy | >= 1.20 | Numerical computing |
| pandas | >= 1.3 | Data manipulation |
| matplotlib | >= 3.4 | Data visualization |
| scipy | >= 1.7 | Scientific computing (Exp 3) |
| pytest | >= 6.2 | Unit testing (Exp 2) |
| requests | >= 2.25 | HTTP requests (Exp 1) |
| streamlit | >= 1.10 | Web dashboard (Exp 1) |

---

## Development Methodology

All experiments follow these principles:

- **AI-Augmented Development**: Code generated and refined with AI assistance, documented in `prompt_log.md`
- **Domain-Driven Validation**: Physical constraints and real-world knowledge applied to validate results
- **Test-Driven Approach**: Comprehensive test coverage for critical calculations
- **Physical Constraints**: All simulations enforce physically meaningful boundary conditions

---

## Results Summary

| Experiment | Status | Key Output |
|------------|--------|------------|
| Exp 1: Rainfall Alert | Complete | Streamlit dashboard + alert log |
| Exp 2: SCS-CN Runoff | Complete | 30+ tests passed, sensitivity analysis plots |
| Exp 3: Reservoir Optimization | Complete | Optimal 7-day schedule, Pareto frontier |
| Exp 4: Flood Inundation | Complete | Flood extent maps, inundation curves |

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- Xi'an Jiaotong University - AI-Augmented Software Engineering Course
- Smart Water Lab Series instructional materials
- OpenWeatherMap API for weather data (Experiment 1)

---

> **Note**: This repository is created for academic purposes as part of the coursework requirements at Xi'an Jiaotong University.

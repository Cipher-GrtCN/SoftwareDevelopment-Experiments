# Experiment 1: Short-term Rainfall Forecasting & Alert System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/API-OpenWeatherMap-yellow.svg" alt="OpenWeatherMap">
  <img src="https://img.shields.io/badge/Dashboard-Streamlit-red.svg" alt="Streamlit">
</p>

A real-time rainfall monitoring system that integrates external weather APIs, implements threshold-based alerting logic for rainfall intensity, and provides an interactive Streamlit dashboard for visualization.

---

## Table of Contents

- [Overview](#overview)
- [Physical Background](#physical-background)
- [File Structure](#file-structure)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
  - [Streamlit Dashboard Mode](#streamlit-dashboard-mode)
  - [Command Line Mode](#command-line-mode)
- [Alert Thresholds](#alert-thresholds)
- [Configuration](#configuration)
- [Results](#results)
- [Implementation Details](#implementation-details)

---

## Overview

This experiment demonstrates:
- Integration of external weather APIs (OpenWeatherMap) using Python `requests`
- Implementation of threshold-based alerting logic for rainfall monitoring
- Building a real-time monitoring dashboard with Streamlit
- Application of domain knowledge to validate physical results

**Course**: AI-Augmented Software Engineering - Smart Water Lab Series  
**Date**: 2026-07-07

---

## Physical Background

Short-term rainfall forecasting (Nowcasting) covers 0-6 hours ahead and is critical for urban flood management. The China Meteorological Administration defines rainfall intensity categories:

| Category | Intensity (mm/h) | Alert Level |
|----------|-----------------|-------------|
| Light | < 2.5 | Green |
| Moderate | 2.5 - 8 | Blue |
| Heavy | 8 - 16 | Yellow |
| Violent | >= 16 | Red |

**System Alert Thresholds:**
- GREEN: Rainfall < 10 mm/h (Normal)
- YELLOW: 10 <= Rainfall < 20 mm/h (Moderate)
- RED: Rainfall >= 20 mm/h (Heavy - ALERT)

---

## File Structure

```
Experiment1_Rainfall_Alert/
├── weather_monitor.py      # Main application (API + Alert + Dashboard)
├── alert_log.txt           # Alert event log with timestamps
├── requirements.txt        # Python dependencies
├── experiment_report.md    # Detailed experiment report
└── prompt_log.md           # AI interaction documentation
```

### File Descriptions

| File | Description |
|------|-------------|
| `weather_monitor.py` | Main application containing API integration, alert logic, Streamlit dashboard, and CLI mode |
| `alert_log.txt` | Log file recording RED alert events with timestamps |
| `requirements.txt` | Python package dependencies |
| `experiment_report.md` | Full experiment report with methodology and results |
| `prompt_log.md` | Documentation of AI-assisted code generation process |

---

## Dependencies

### Required Packages

| Package | Version | Purpose |
|---------|---------|---------|
| Python | >= 3.8 | Programming language |
| requests | >= 2.25 | HTTP requests to OpenWeatherMap API |
| streamlit | >= 1.10 | Interactive web dashboard |
| pandas | >= 1.3 | Data manipulation for alert logs |
| matplotlib | >= 3.4 | Forecast chart visualization |

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install requests streamlit pandas matplotlib
```

---

## Installation

```bash
# Clone the repository (if not already cloned)
git clone https://github.com/Cipher-GrtCN/SoftwareDevelopment-Experiments.git

# Navigate to this experiment
cd SoftwareDevelopment-Experiments/Experiment1_Rainfall_Alert

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Streamlit Dashboard Mode

Launch the interactive web dashboard:

```bash
streamlit run weather_monitor.py -- --streamlit
```

Or:
```bash
streamlit run weather_monitor.py
```

The dashboard provides:
- **City selector** - Enter any city name to monitor
- **Current rainfall display** - Real-time rainfall intensity with alert status
- **7-period forecast chart** - Color-coded bar chart with alert thresholds
- **Alert history log** - Table of all RED alert events with timestamps
- **Physical validation checks** - Automated validation of physical constraints
- **Auto-refresh** - Optional automatic data refresh at configurable intervals

> **Note**: If no OpenWeatherMap API key is provided, the system automatically runs in **Demo Mode** with simulated data for Beijing, Shanghai, Guangzhou, Shenzhen, and Chengdu.

### Command Line Mode

Run the monitor in terminal mode:

```bash
# Monitor default city (Beijing) for 30 seconds
python weather_monitor.py

# Monitor a specific city
python weather_monitor.py Shanghai

# The CLI mode runs for 30 seconds with 5-second intervals by default
```

### API Key Setup (Optional)

For real weather data, obtain a free API key from [OpenWeatherMap](https://openweathermap.org/api):

```bash
# Set as environment variable
export OPENWEATHER_API_KEY="your_api_key_here"

# Or enter directly in the Streamlit sidebar when running the dashboard
```

**API Limitations:**
- Free tier: 60 calls/minute, 1,000 calls/day
- API may return 0 rainfall when it's not actually raining
- Rain data field may be missing in the response when there is no precipitation

---

## Alert Thresholds

The system uses a three-tier alert system based on rainfall intensity:

| Level | Condition | Color | Action |
|-------|-----------|-------|--------|
| GREEN | < 10 mm/h | #28a745 | Normal monitoring |
| YELLOW | 10 - 20 mm/h | #ffc107 | Moderate rain warning |
| RED | >= 20 mm/h | #dc3545 | **ALERT** - Logged to file |

When a RED alert is triggered, the event is automatically logged to `alert_log.txt` with a timestamp.

---

## Configuration

Key configuration options in `weather_monitor.py`:

```python
# API Configuration
API_KEY = os.environ.get("OPENWEATHER_API_KEY", "your_api_key_here")
API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Alert Thresholds (mm/h)
THRESHOLDS = {
    "GREEN": {"max": 10, "label": "Normal"},
    "YELLOW": {"min": 10, "max": 20, "label": "Moderate"},
    "RED": {"min": 20, "label": "Heavy - ALERT"},
}

# Logging
LOG_FILE = "alert_log.txt"
```

---

## Results

### Alert Logic Validation

| Test Case | Rainfall (mm/h) | Expected Alert | Result |
|-----------|----------------|----------------|--------|
| No rain | 0 | GREEN | PASS |
| Light rain | 5 | GREEN | PASS |
| Boundary | 10 | YELLOW | PASS |
| Moderate | 15 | YELLOW | PASS |
| Heavy | 25 | RED | PASS |
| Invalid | -5 | Error | PASS |

### Physical Validation
- All rainfall values are non-negative
- Alert thresholds correctly applied at all boundaries
- Log file records timestamps accurately
- Demo mode provides realistic test data without API key

---

## Implementation Details

### Core Functions

| Function | Description |
|----------|-------------|
| `fetch_weather_data(city, api_key)` | Fetch weather data from API or demo mode |
| `check_alert(rainfall)` | Determine alert level based on rainfall intensity |
| `log_alert(alert_info, city)` | Log RED alert events to file with timestamp |
| `read_alert_log()` | Read alert log as pandas DataFrame |
| `create_dashboard()` | Build Streamlit dashboard interface |
| `run_cli_monitor(city, duration, interval)` | Run command-line monitoring mode |

### Error Handling

The system handles the following error cases:
- Invalid API key (HTTP 401)
- City not found (HTTP 404)
- Network connection errors
- Request timeouts
- Missing rain data in API response
- Negative rainfall values (physical validation)

---

## Student Information

| Item | Details |
|------|---------|
| **Name** | 凌心阳 (Ling Xinyang) |
| **Student ID** | 3125301135 |
| **Course** | AI-Augmented Software Engineering |

---

> **Note**: This experiment is part of the Smart Water Lab Series coursework at Xi'an Jiaotong University.

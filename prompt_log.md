# Prompt Log - Experiment 1: Rainfall Forecasting & Alert System

## Experiment Overview
**Date**: 2026-07-07
**Student**: AI-Assisted Development
**Experiment**: Short-term Rainfall Forecasting & Alert System
**Duration**: 2 hours

---

## AI Interaction Log

### Prompt 1: API Integration Code Generation

**Role**: Water Resources Engineering Student
**Context**: Building a rainfall monitoring system for urban flood management
**Task**: Write Python code to fetch weather data from OpenWeatherMap API
**Constraints**: Must handle errors, include comments, use requests library

**Prompt Used**:
```
I am a water resources student building a rainfall monitoring system.
Please write Python code to fetch current weather data for Beijing
using the OpenWeatherMap API. The code should:
1. Use the requests library to make the API call
2. Extract rainfall intensity from the response
3. Handle API errors gracefully (invalid key, network error, city not found)
4. Include comments explaining each step
5. Return a structured dictionary with all relevant data
```

**AI Response Summary**:
- Generated a `fetch_weather_data()` function with comprehensive error handling
- Included HTTP status code checks (401, 404, timeout)
- Added type hints and docstring
- Suggested using demo mode when API key is unavailable

**Verification Steps**:
1. ✅ Checked that all error types are handled
2. ✅ Verified rainfall extraction from API response format
3. ✅ Tested with invalid API key - returns appropriate error message
4. ✅ Tested with non-existent city - returns 404 error
5. ✅ Physical validation: rainfall values are non-negative

**Corrections Made**:
- Added demo mode with simulated data for testing without API key
- Enhanced error messages with specific guidance
- Added rainfall intensity calculation from 1h rain volume

---

### Prompt 2: Alert Logic Implementation

**Role**: Hydrological Engineer
**Context**: Implementing threshold-based alerting for urban flood management
**Task**: Create alert system with color-coded levels based on rainfall intensity
**Constraints**: Must follow China Meteorological Administration standards

**Prompt Used**:
```
Implement a threshold-based rainfall alert system in Python with:
1. Three alert levels: GREEN (<10mm/h), YELLOW (10-20mm/h), RED (≥20mm/h)
2. A check_alert(rainfall) function that returns alert level, color code, and message
3. Input validation (rainfall must be non-negative)
4. Logging function that writes RED alerts to a file with timestamps
5. Physical constraint validation
```

**AI Response Summary**:
- Generated `check_alert()` function with proper threshold logic
- Created `log_alert()` function with timestamp formatting
- Included input validation with ValueError for negative values

**Verification Steps**:
1. ✅ Tested boundary: rainfall=9.9 → GREEN
2. ✅ Tested boundary: rainfall=10.0 → YELLOW
3. ✅ Tested boundary: rainfall=19.9 → YELLOW
4. ✅ Tested boundary: rainfall=20.0 → RED
5. ✅ Tested edge case: rainfall=0 → GREEN
6. ✅ Tested invalid: rainfall=-5 → ValueError raised
7. ✅ Verified log file format and timestamp correctness

**Corrections Made**:
- Refined threshold definitions to use explicit boundary values
- Added emoji indicators for better visual feedback
- Enhanced log format with structured fields

---

### Prompt 3: Streamlit Dashboard Creation

**Role**: Data Visualization Engineer
**Context**: Building monitoring dashboard for real-time rainfall data
**Task**: Create Streamlit dashboard with metrics, charts, and alert history
**Constraints**: Must be responsive, include auto-refresh, display physical validation

**Prompt Used**:
```
Create a Streamlit dashboard for rainfall monitoring with:
1. Title and description
2. City input selector
3. Large metric display for current rainfall
4. Color-coded alert status indicator
5. Bar chart showing rainfall forecast
6. Alert history table
7. Physical validation checks display
8. Auto-refresh capability
```

**AI Response Summary**:
- Generated complete Streamlit dashboard code
- Included sidebar with settings
- Created responsive layout with columns
- Added forecast visualization with threshold lines

**Verification Steps**:
1. ✅ Verified layout renders correctly
2. ✅ Tested metric display updates with different values
3. ✅ Confirmed alert colors match threshold logic
4. ✅ Validated chart shows correct data points
5. ✅ Checked auto-refresh functionality

**Corrections Made**:
- Added demo mode indicator in sidebar
- Enhanced physical validation section
- Improved forecast chart with value labels

---

### Prompt 4: Code Review and Refinement

**Role**: Code Reviewer
**Context**: Final review of complete rainfall monitoring system
**Task**: Review code for quality, documentation, and correctness
**Constraints**: Must follow Python 3.12+ standards, include type hints

**Prompt Used**:
```
Review the following rainfall monitoring code for:
1. Code quality and structure
2. Documentation completeness
3. Error handling coverage
4. Physical correctness of hydrological logic
5. Suggest improvements
```

**AI Response Summary**:
- Confirmed proper function decomposition
- Verified docstring completeness
- Validated error handling patterns
- Confirmed physical constraints are enforced

**Verification Steps**:
1. ✅ All functions have type hints
2. ✅ All functions have docstrings
3. ✅ Error handling covers all expected cases
4. ✅ Physical constraints are validated
5. ✅ Code follows PEP 8 style

---

## Key Learnings

1. **AI Strengths**: Code generation speed, error handling patterns, documentation
2. **AI Weaknesses**: Physical domain knowledge requires human verification
3. **Human-in-the-Loop**: Essential for validating hydrological constraints
4. **Swiss Cheese Model**: Multiple validation layers (syntax → logic → physical)

## Time Breakdown
- API Integration: 30 min
- Alert Logic: 30 min
- Dashboard Creation: 40 min
- Testing & Validation: 20 min

## Files Created
1. `weather_monitor.py` - Main application (338 lines)
2. `alert_log.txt` - Alert log file
3. `prompt_log.md` - This file

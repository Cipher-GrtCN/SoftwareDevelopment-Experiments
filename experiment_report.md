# Experiment 1: Short-term Rainfall Forecasting & Alert System

## Experiment Information
- **Course**: AI-Augmented Software Engineering
- **Module**: Smart Water Lab Series - Week 5 Session A
- **Duration**: 2 hours
- **Date**: 2026-07-07

---

## 1. Experiment Objectives

1. Integrate external weather APIs (OpenWeatherMap) using AI assistance
2. Implement threshold-based alerting logic for rainfall monitoring
3. Build a real-time monitoring dashboard with Streamlit
4. Apply domain knowledge to validate results

---

## 2. Physical Background

Short-term rainfall forecasting (Nowcasting) covers 0-6 hours ahead and is critical for urban flood management. The China Meteorological Administration defines rainfall intensity categories:

| Category | Intensity (mm/h) | Alert Level |
|----------|-----------------|-------------|
| Light | < 2.5 | Green |
| Moderate | 2.5 - 8 | Blue |
| Heavy | 8 - 16 | Yellow |
| Violent | >= 16 | Red |

**Alert Thresholds Used:**
- GREEN: Rainfall < 10 mm/h (Normal)
- YELLOW: 10 <= Rainfall < 20 mm/h (Moderate)
- RED: Rainfall >= 20 mm/h (Heavy - ALERT)

---

## 3. Methodology

### 3.1 API Integration
- Used OpenWeatherMap API for real-time weather data
- Implemented error handling for network issues, invalid keys, city not found
- Added demo mode with simulated data for testing without API key

### 3.2 Alert Logic
- Implemented `check_alert(rainfall)` function with three-tier threshold system
- Added `log_alert()` function to record RED alerts with timestamps
- Physical validation: rainfall must be non-negative

### 3.3 Dashboard
- Built Streamlit dashboard with:
  - City selector
  - Current rainfall display with alert status
  - 7-period forecast bar chart with color-coded alert levels
  - Alert history log table
  - Physical validation checks

---

## 4. Results

### 4.1 API Integration Test
- Successfully fetched weather data for multiple cities
- Error handling works correctly for all error types
- Demo mode provides realistic test data

### 4.2 Alert Logic Validation
| Test Case | Rainfall (mm/h) | Expected Alert | Result |
|-----------|----------------|----------------|--------|
| No rain | 0 | GREEN | PASS |
| Light rain | 5 | GREEN | PASS |
| Boundary | 10 | YELLOW | PASS |
| Moderate | 15 | YELLOW | PASS |
| Heavy | 25 | RED | PASS |
| Invalid | -5 | Error | PASS |

### 4.3 Physical Validation
- All rainfall values are non-negative
- Alert thresholds correctly applied
- Log file records timestamps accurately

---

## 5. Files Delivered

| File | Description |
|------|-------------|
| `weather_monitor.py` | Main application (API + Alert + Dashboard) |
| `alert_log.txt` | Alert event log with timestamps |
| `prompt_log.md` | AI interaction documentation |
| `requirements.txt` | Python dependencies |

---

## 6. Discussion

### AI Collaboration Insights
- AI successfully generated API integration code with comprehensive error handling
- Physical validation (rainfall >= 0) was added based on domain knowledge
- Demo mode was necessary for testing without a real API key

### Challenges
- OpenWeatherMap free tier has rate limits (60 calls/min)
- API may return 0 rainfall when it's not actually raining
- Required careful handling of missing rain data in API response

### Conclusion
Successfully built a functional rainfall monitoring system with threshold-based alerting. The system integrates weather APIs, implements proper alert logic, and provides a user-friendly dashboard.

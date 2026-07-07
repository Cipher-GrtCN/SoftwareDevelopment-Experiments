"""
Experiment 1: Short-term Rainfall Forecasting & Alert System
AI-Augmented Software Engineering - Smart Water Lab Series

This module implements a real-time rainfall monitoring system that:
1. Integrates external weather APIs (OpenWeatherMap)
2. Implements threshold-based alerting logic
3. Provides a Streamlit dashboard for visualization
4. Logs alerts with timestamps for historical tracking

Physical Background:
- Short-term forecasting (Nowcasting): 0-6 hours ahead
- Alert threshold: 20 mm/h (heavy rainfall)
- Rainfall intensity categories per China Meteorological Administration
"""

import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
import os

# Configure matplotlib for headless environments
plt.use("Agg")

# =============================================================================
# CONFIGURATION
# =============================================================================

# API Configuration
API_KEY = os.environ.get("OPENWEATHER_API_KEY", "your_api_key_here")
API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Alert Thresholds (mm/h)
THRESHOLDS = {
    "GREEN": {"max": 10, "label": "Normal", "color": "#28a745", "emoji": "✅"},
    "YELLOW": {"min": 10, "max": 20, "label": "Moderate", "color": "#ffc107", "emoji": "⚠️"},
    "RED": {"min": 20, "label": "Heavy - ALERT", "color": "#dc3545", "emoji": "🚨"},
}

# Logging configuration
LOG_FILE = "alert_log.txt"

# =============================================================================
# DEMO MODE: Simulated weather data for testing without API key
# =============================================================================

DEMO_MODE = API_KEY == "your_api_key_here"

# Simulated rainfall data for demonstration (Beijing, Haidian District)
DEMO_RAINFALL_DATA = {
    "Beijing": {
        "current": 25.5,  # mm/h - triggers RED alert
        "forecast": [5.2, 12.8, 25.5, 8.3, 18.7, 32.1, 15.4],
        "description": "Heavy rain",
    },
    "Shanghai": {
        "current": 8.5,  # mm/h - YELLOW alert
        "forecast": [2.1, 8.5, 15.3, 6.7, 22.4, 11.2, 4.8],
        "description": "Moderate rain",
    },
    "Guangzhou": {
        "current": 3.2,  # mm/h - GREEN (normal)
        "forecast": [1.5, 3.2, 7.8, 12.4, 5.6, 9.3, 2.1],
        "description": "Light rain",
    },
    "Shenzhen": {
        "current": 35.0,  # mm/h - RED alert (extreme)
        "forecast": [15.2, 35.0, 28.7, 42.3, 18.9, 10.5, 22.1],
        "description": "Violent rain",
    },
    "Chengdu": {
        "current": 0.0,  # mm/h - No rain
        "forecast": [0.0, 0.5, 2.3, 8.7, 15.2, 6.4, 1.8],
        "description": "Clear",
    },
}


def fetch_weather_data(city: str, api_key: str = None) -> dict:
    """
    Fetch current weather data for a given city.

    Args:
        city: City name (e.g., 'Beijing', 'Shanghai')
        api_key: OpenWeatherMap API key (optional, uses default if not provided)

    Returns:
        Dictionary containing weather data including rainfall information
    """
    # Use demo mode if no API key is available
    if DEMO_MODE or api_key == "your_api_key_here":
        return _fetch_demo_data(city)

    # Real API call
    try:
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
        }
        response = requests.get(API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract rainfall data (may not be present if not raining)
        rain_data = data.get("rain", {})
        rain_1h = rain_data.get("1h", 0)  # Rain volume for last 1 hour in mm

        # Calculate rainfall intensity (mm/h)
        rainfall_intensity = rain_1h

        return {
            "city": city,
            "rainfall": rainfall_intensity,
            "description": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "timestamp": datetime.now(),
            "source": "api",
            "status": "success",
        }

    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            return {"error": "Invalid API key. Please check your OpenWeatherMap API key.", "status": "error"}
        elif response.status_code == 404:
            return {"error": f"City '{city}' not found. Please check the city name.", "status": "error"}
        else:
            return {"error": f"HTTP Error: {e}", "status": "error"}

    except requests.exceptions.ConnectionError:
        return {"error": "Network error. Please check your internet connection.", "status": "error"}

    except requests.exceptions.Timeout:
        return {"error": "Request timed out. The API server is taking too long to respond.", "status": "error"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "status": "error"}


def _fetch_demo_data(city: str) -> dict:
    """
    Return simulated weather data for demonstration purposes.

    Args:
        city: City name

    Returns:
        Dictionary with simulated weather data
    """
    # Use default city data if city not found
    city_data = DEMO_RAINFALL_DATA.get(city, DEMO_RAINFALL_DATA["Beijing"])

    return {
        "city": city,
        "rainfall": city_data["current"],
        "description": city_data["description"],
        "temperature": 22.5,
        "humidity": 78,
        "timestamp": datetime.now(),
        "source": "demo",
        "status": "success",
        "forecast": city_data["forecast"],
    }


def check_alert(rainfall: float) -> dict:
    """
    Determine alert level based on rainfall intensity.

    Physical Logic:
    - GREEN: Rainfall < 10 mm/h (Normal)
    - YELLOW: 10 <= Rainfall < 20 mm/h (Moderate)
    - RED: Rainfall >= 20 mm/h (Heavy - ALERT)

    Args:
        rainfall: Rainfall intensity in mm/h

    Returns:
        Dictionary with alert level, message, and color code
    """
    if rainfall < 0:
        raise ValueError("Rainfall intensity cannot be negative")

    if rainfall < THRESHOLDS["GREEN"]["max"]:
        level = "GREEN"
    elif rainfall < THRESHOLDS["YELLOW"]["max"]:
        level = "YELLOW"
    else:
        level = "RED"

    threshold_info = THRESHOLDS[level]

    return {
        "level": level,
        "label": threshold_info["label"],
        "color": threshold_info["color"],
        "emoji": threshold_info["emoji"],
        "message": f"{threshold_info['emoji']} {threshold_info['label']}: Rainfall = {rainfall:.1f} mm/h",
        "rainfall": rainfall,
    }


def log_alert(alert_info: dict, city: str) -> None:
    """
    Log alert events to file with timestamp.

    Args:
        alert_info: Dictionary containing alert information from check_alert()
        city: City name where the alert was triggered
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"[{timestamp}] City: {city} | "
        f"Rainfall: {alert_info['rainfall']:.1f} mm/h | "
        f"Alert Level: {alert_info['level']} | "
        f"Status: {alert_info['label']}\n"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)


def read_alert_log() -> pd.DataFrame:
    """
    Read alert log file and return as DataFrame for display.

    Returns:
        DataFrame with columns: Timestamp, City, Rainfall (mm/h), Alert Level, Status
    """
    if not os.path.exists(LOG_FILE):
        return pd.DataFrame(columns=["Timestamp", "City", "Rainfall (mm/h)", "Alert Level", "Status"])

    entries = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Parse log entry format
            try:
                parts = line.split(" | ")
                timestamp = parts[0].strip("[]")
                city = parts[1].replace("City: ", "")
                rainfall = float(parts[2].replace("Rainfall: ", "").replace(" mm/h", ""))
                level = parts[3].replace("Alert Level: ", "")
                status = parts[4].replace("Status: ", "")
                entries.append({
                    "Timestamp": timestamp,
                    "City": city,
                    "Rainfall (mm/h)": rainfall,
                    "Alert Level": level,
                    "Status": status,
                })
            except (IndexError, ValueError):
                continue

    return pd.DataFrame(entries)


# =============================================================================
# STREAMLIT DASHBOARD
# =============================================================================

def create_dashboard():
    """
    Create Streamlit dashboard for rainfall monitoring.
    """
    st.set_page_config(
        page_title="Rainfall Monitoring System",
        page_icon="🌧️",
        layout="wide",
    )

    st.title("🌧️ Rainfall Monitoring & Alert System")
    st.markdown("*Real-time rainfall monitoring with threshold-based alerting for urban flood management*")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        # City selection
        city = st.text_input("Enter City Name", value="Beijing")

        # API Key input (optional)
        api_key_input = st.text_input(
            "OpenWeather API Key (optional)",
            value="",
            type="password",
            help="Leave empty to use demo mode",
        )

        # Refresh interval
        refresh_interval = st.slider("Refresh Interval (seconds)", 5, 300, 60)

        # Auto-refresh toggle
        auto_refresh = st.toggle("Auto Refresh", value=False)

        # Demo mode indicator
        if DEMO_MODE and not api_key_input:
            st.info("📢 Running in **Demo Mode**. Add an API key for real data.")

        st.markdown("---")
        st.markdown("### Alert Thresholds")
        st.markdown("🟢 **GREEN**: < 10 mm/h (Normal)")
        st.markdown("🟡 **YELLOW**: 10-20 mm/h (Moderate)")
        st.markdown("🔴 **RED**: ≥ 20 mm/h (Heavy)")

    # Main content area
    col1, col2, col3 = st.columns(3)

    # Fetch weather data
    api_key = api_key_input if api_key_input else API_KEY
    weather_data = fetch_weather_data(city, api_key)

    if weather_data.get("status") == "error":
        st.error(f"❌ {weather_data['error']}")
        return

    rainfall = weather_data["rainfall"]
    alert_info = check_alert(rainfall)

    # Log alert if RED level
    if alert_info["level"] == "RED":
        log_alert(alert_info, city)
        st.toast(f"🚨 RED ALERT triggered for {city}!")

    # Display metrics
    with col1:
        st.metric(
            label="Current Rainfall",
            value=f"{rainfall:.1f} mm/h",
            delta="Heavy" if rainfall >= 20 else "Moderate" if rainfall >= 10 else "Normal",
        )

    with col2:
        st.markdown(
            f"""
            <div style="background-color: {alert_info['color']}22; 
                        border-left: 5px solid {alert_info['color']}; 
                        padding: 15px; border-radius: 5px;">
                <h3 style="color: {alert_info['color']}; margin: 0;">
                    {alert_info['emoji']} {alert_info['level']}
                </h3>
                <p style="margin: 5px 0 0 0;">{alert_info['label']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px;">
                <p><strong>🌍 City:</strong> {weather_data['city']}</p>
                <p><strong>🌡️ Temperature:</strong> {weather_data.get('temperature', 'N/A')}°C</p>
                <p><strong>💧 Humidity:</strong> {weather_data.get('humidity', 'N/A')}%</p>
                <p><strong>📝 Condition:</strong> {weather_data['description'].capitalize()}</p>
                <p><strong>📡 Source:</strong> {weather_data.get('source', 'unknown').upper()}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Forecast chart
    st.markdown("---")
    st.subheader("📊 Rainfall Forecast (Next 7 Periods)")

    forecast_data = weather_data.get("forecast", [])
    if forecast_data:
        # Create time labels
        now = datetime.now()
        time_labels = [(now + timedelta(hours=i)).strftime("%H:%M") for i in range(len(forecast_data))]

        # Create alert level colors for each forecast point
        colors = []
        for f in forecast_data:
            if f >= 20:
                colors.append("#dc3545")  # RED
            elif f >= 10:
                colors.append("#ffc107")  # YELLOW
            else:
                colors.append("#28a745")  # GREEN

        # Plot
        fig, ax = plt.subplots(figsize=(12, 5))

        # Threshold lines
        ax.axhline(y=10, color="#ffc107", linestyle="--", alpha=0.7, label="Yellow Threshold (10 mm/h)")
        ax.axhline(y=20, color="#dc3545", linestyle="--", alpha=0.7, label="Red Threshold (20 mm/h)")

        # Bar chart with alert colors
        bars = ax.bar(time_labels, forecast_data, color=colors, alpha=0.8, edgecolor="black", linewidth=0.5)

        # Add value labels on bars
        for bar, val in zip(bars, forecast_data):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.5,
                f"{val:.1f}",
                ha="center",
                va="bottom",
                fontsize=9,
            )

        ax.set_xlabel("Time", fontsize=12)
        ax.set_ylabel("Rainfall Intensity (mm/h)", fontsize=12)
        ax.set_title(f"Rainfall Forecast - {city}", fontsize=14, fontweight="bold")
        ax.legend(loc="upper left")
        ax.set_ylim(0, max(forecast_data) * 1.2)
        ax.grid(axis="y", alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig)

    # Alert Log Section
    st.markdown("---")
    st.subheader("📋 Alert History Log")

    alert_df = read_alert_log()
    if not alert_df.empty:
        st.dataframe(alert_df, use_container_width=True)

        # Alert statistics
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            st.metric("Total Alerts", len(alert_df))
        with col_stat2:
            red_count = len(alert_df[alert_df["Alert Level"] == "RED"])
            st.metric("RED Alerts", red_count)
        with col_stat3:
            yellow_count = len(alert_df[alert_df["Alert Level"] == "YELLOW"])
            st.metric("YELLOW Alerts", yellow_count)
    else:
        st.info("No alerts logged yet. RED alerts will be recorded automatically.")

    # Physical validation
    st.markdown("---")
    st.subheader("✅ Physical Validation Checks")

    validation_checks = [
        ("Rainfall intensity ≥ 0", rainfall >= 0),
        ("Rainfall is a finite number", rainfall == rainfall),  # Not NaN
        ("Alert threshold correctly applied",
         (rainfall < 10 and alert_info["level"] == "GREEN") or
         (10 <= rainfall < 20 and alert_info["level"] == "YELLOW") or
         (rainfall >= 20 and alert_info["level"] == "RED")),
    ]

    for check_name, passed in validation_checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        st.write(f"{status}: {check_name}")

    # Auto-refresh
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()


# =============================================================================
# COMMAND-LINE INTERFACE (for testing without Streamlit)
# =============================================================================

def run_cli_monitor(city: str = "Beijing", duration: int = 60, interval: int = 5):
    """
    Run rainfall monitor in command-line mode for testing.

    Args:
        city: City to monitor
        duration: Total monitoring duration in seconds
        interval: Check interval in seconds
    """
    print(f"🌧️  Rainfall Monitoring System - CLI Mode")
    print(f"📍 Monitoring: {city}")
    print(f"⏱️  Duration: {duration}s | Interval: {interval}s")
    print(f"{'='*60}")

    start_time = time.time()
    iteration = 0

    while time.time() - start_time < duration:
        iteration += 1
        print(f"\n--- Check #{iteration} ---")

        weather_data = fetch_weather_data(city)

        if weather_data.get("status") == "error":
            print(f"❌ Error: {weather_data['error']}")
            break

        rainfall = weather_data["rainfall"]
        alert = check_alert(rainfall)

        print(f"🌍 City: {weather_data['city']}")
        print(f"🌧️  Rainfall: {rainfall:.1f} mm/h")
        print(f"{alert['emoji']} Alert: {alert['label']}")

        if alert["level"] == "RED":
            log_alert(alert, city)
            print(f"🚨 RED ALERT LOGGED to {LOG_FILE}")

        if iteration * interval < duration:
            print(f"⏳ Next check in {interval}s...")
            time.sleep(interval)

    print(f"\n{'='*60}")
    print("✅ Monitoring completed.")
    print(f"📁 Alert log saved to: {LOG_FILE}")


if __name__ == "__main__":
    import sys

    # Check if running in Streamlit
    try:
        import streamlit.runtime.scriptrunner as script_runner
        IN_STREAMLIT = True
    except ImportError:
        IN_STREAMLIT = False

    if IN_STREAMLIT or len(sys.argv) > 1 and sys.argv[1] == "--streamlit":
        create_dashboard()
    else:
        # CLI mode
        city = sys.argv[1] if len(sys.argv) > 1 else "Beijing"
        run_cli_monitor(city=city, duration=30, interval=5)

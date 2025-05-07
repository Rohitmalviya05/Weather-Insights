"""
Visualization service for creating charts and exporting data.
"""

import os
import logging
import csv
import json
from datetime import datetime, timedelta

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Constants
CHARTS_DIR = os.path.join('static', 'charts')
EXPORTS_DIR = os.path.join('static', 'exports')


def analyze_health_trends(csv_file):
    """
    Analyze health trends from scraped weather data
    Returns visualization data for temperature, humidity, and overall health risk
    """
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        from datetime import datetime
        
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        # Create health risk charts directory if it doesn't exist
        charts_dir = os.path.join('static', 'charts', 'health')
        os.makedirs(charts_dir, exist_ok=True)
        
        # Generate temperature trend chart
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df, x='date', y='temperature', marker='o')
        plt.title('Temperature Trends')
        plt.xticks(rotation=45)
        plt.tight_layout()
        temp_chart = os.path.join(charts_dir, 'temperature_trend.png')
        plt.savefig(temp_chart)
        plt.close()
        
        # Generate humidity vs health condition chart
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='weather_condition', y='humidity')
        plt.title('Average Humidity by Weather Condition')
        plt.xticks(rotation=45)
        plt.tight_layout()
        humidity_chart = os.path.join(charts_dir, 'humidity_conditions.png')
        plt.savefig(humidity_chart)
        plt.close()
        
        # Calculate health risk metrics
        health_metrics = {
            'high_temp_days': len(df[df['temperature'] > 30]),
            'low_temp_days': len(df[df['temperature'] < 10]),
            'high_humidity_days': len(df[df['humidity'] > 70]),
            'avg_temperature': df['temperature'].mean(),
            'avg_humidity': df['humidity'].mean(),
            'common_conditions': df['weather_condition'].value_counts().to_dict()
        }
        
        return {
            'charts': {
                'temperature': os.path.basename(temp_chart),
                'humidity': os.path.basename(humidity_chart)
            },
            'metrics': health_metrics
        }
        
    except Exception as e:
        logger.error(f"Error analyzing health trends: {e}")
        return None

def get_historical_data(lat, lon, days=30):
    """
    Get historical weather data for a location.
    
    This is mocked data as OpenWeatherMap doesn't provide historical data with their free API.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        days (int): Number of days in the past
        
    Returns:
        dict: Historical weather data
    """
    # Create mock historical data
    historical_data = {
        "success": True,
        "location": {
            "name": get_location_name_from_coords(lat, lon),
            "lat": lat,
            "lon": lon
        },
        "days": []
    }
    
    # Generate data points
    current_date = datetime.now()
    
    # Base values
    base_temp = 22
    base_temp_min = 18
    base_temp_max = 26
    base_humidity = 65
    base_pressure = 1013
    base_wind_speed = 4.5
    
    # Create a sinusoidal pattern for temperature variation over time
    for i in range(days, 0, -1):
        day_date = current_date - timedelta(days=i)
        
        # Add some cyclical and random variation
        day_offset = (i % 7) / 7.0  # Weekly cycle
        season_offset = abs(days/2 - i) / (days/2)  # Season trend
        
        temp = base_temp + (3 * season_offset) + (2 * day_offset) + ((-1) ** i)
        temp_min = base_temp_min + (3 * season_offset) + (1.5 * day_offset) + ((-1) ** i)
        temp_max = base_temp_max + (4 * season_offset) + (2.5 * day_offset) + ((-1) ** i)
        
        # Humidity inversely correlated with temperature on average
        humidity = base_humidity - (10 * season_offset) + (5 * day_offset) + ((-1) ** i * 2)
        humidity = max(30, min(90, humidity))  # Clamp between 30% and 90%
        
        # Pressure variations (less dramatic)
        pressure = base_pressure + ((-1) ** i * 2) + (day_offset * 3)
        
        # Wind speed (more random)
        wind_speed = base_wind_speed + (day_offset * 3) + (i % 3)
        
        # Weather condition (simplified patterns)
        weather_conditions = ["Clear", "Partly Cloudy", "Cloudy", "Light Rain", "Rain"]
        condition_index = int((i + day_offset * 10) % len(weather_conditions))
        condition = weather_conditions[condition_index]
        
        # Create day entry
        day_data = {
            "dt": int(day_date.timestamp()),
            "date": day_date.strftime("%Y-%m-%d"),
            "day": day_date.strftime("%a"),
            "temp": temp,
            "temp_min": temp_min,
            "temp_max": temp_max,
            "humidity": humidity,
            "pressure": pressure,
            "wind_speed": wind_speed,
            "condition": condition
        }
        
        historical_data["days"].append(day_data)
    
    return historical_data


def export_data_to_csv(data, location_name, type_name="historical"):
    """
    Export data to CSV file.
    
    Args:
        data (dict): Data to export
        location_name (str): Location name for the filename
        type_name (str): Type of data for the filename
        
    Returns:
        str: Path to the CSV file relative to 'static'
    """
    # Ensure exports directory exists
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    
    # Sanitize location name for filename
    safe_location = "".join(c for c in location_name if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_location}_{type_name}_{timestamp}.csv"
    filepath = os.path.join(EXPORTS_DIR, filename)
    
    try:
        # Extract data points based on type
        if type_name == "historical" and "days" in data:
            fieldnames = ["date", "day", "temp", "temp_min", "temp_max", 
                         "humidity", "pressure", "wind_speed", "condition"]
            rows = data["days"]
        elif type_name == "forecast" and "forecast" in data:
            fieldnames = ["date", "day", "temp_avg", "temp_min", "temp_max", 
                         "humidity_avg", "rain_chance", "wind_speed_avg", "weather_description"]
            
            # Transform forecast data to match CSV format
            rows = []
            for day in data["forecast"]:
                row = {
                    "date": day["date"],
                    "day": day["day"],
                    "temp_avg": day["temp_avg"],
                    "temp_min": day["temp_min"],
                    "temp_max": day["temp_max"],
                    "humidity_avg": day["humidity_avg"],
                    "rain_chance": day["rain_chance"],
                    "wind_speed_avg": day["wind_speed_avg"],
                    "weather_description": day["weather"]["description"] if "weather" in day else ""
                }
                rows.append(row)
        else:
            logger.error(f"Unsupported data type for CSV export: {type_name}")
            return None
        
        # Write to CSV
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                # Filter dict to only include fields in fieldnames
                filtered_row = {k: row[k] for k in fieldnames if k in row}
                writer.writerow(filtered_row)
        
        # Return relative path for URL
        relative_path = os.path.join(os.path.basename(EXPORTS_DIR), filename)
        return relative_path
    
    except Exception as e:
        logger.error(f"Error exporting data to CSV: {e}")
        return None


def create_temperature_chart(location_name, data, chart_type="temperature"):
    """
    Create a temperature chart for the given data.
    
    Args:
        location_name (str): Location name for the chart title
        data (dict): Data for the chart
        chart_type (str): Type of chart to create
        
    Returns:
        str: Path to the chart image relative to 'static'
    """
    # Ensure charts directory exists
    os.makedirs(CHARTS_DIR, exist_ok=True)
    
    # Sanitize location name for filename
    safe_location = "".join(c for c in location_name if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_location}_{chart_type}_{timestamp}.png"
    filepath = os.path.join(CHARTS_DIR, filename)
    
    try:
        # Get chart data based on type
        if chart_type == "temperature" and "days" in data:
            # Extract data for temperature chart
            dates = []
            temps = []
            temp_mins = []
            temp_maxs = []
            
            for day in data["days"]:
                date = datetime.fromtimestamp(day["dt"]) if "dt" in day else datetime.strptime(day["date"], "%Y-%m-%d")
                dates.append(date)
                temps.append(day["temp"])
                temp_mins.append(day["temp_min"])
                temp_maxs.append(day["temp_max"])
            
            # Create figure and axes
            plt.figure(figsize=(10, 6))
            ax = plt.gca()
            
            # Plot temperature lines
            plt.plot(dates, temps, 'b-', label='Average', linewidth=2)
            plt.plot(dates, temp_mins, 'c--', label='Min', linewidth=1.5)
            plt.plot(dates, temp_maxs, 'r--', label='Max', linewidth=1.5)
            
            # Fill between min and max
            plt.fill_between(dates, temp_mins, temp_maxs, alpha=0.2, color='orange')
            
            # Set labels and title
            plt.title(f'Temperature Trends for {location_name}', fontsize=16)
            plt.ylabel('Temperature (°C)', fontsize=12)
            plt.xlabel('Date', fontsize=12)
            
            # Format the x-axis to show dates nicely
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            if len(dates) > 14:
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
            else:
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
            plt.xticks(rotation=45)
            
            # Add grid and legend
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend()
            
            # Adjust layout and save
            plt.tight_layout()
            plt.savefig(filepath, dpi=100)
            plt.close()
            
            # Return relative path for URL
            relative_path = os.path.join(os.path.basename(CHARTS_DIR), filename)
            return relative_path
            
        else:
            logger.error(f"Unsupported chart type: {chart_type}")
            return None
    
    except Exception as e:
        logger.error(f"Error creating chart: {e}")
        return None


def get_location_name_from_coords(lat, lon):
    """
    Get a location name from coordinates.
    This is a simple approximation function for when reverse geocoding is not available.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        
    Returns:
        str: Approximate location name
    """
    # Very simple approximation
    location_name = "Unknown Location"
    
    # Check for some known locations
    if abs(lat - 51.5074) < 0.5 and abs(lon - (-0.1278)) < 0.5:
        location_name = "London"
    elif abs(lat - 40.7128) < 0.5 and abs(lon - (-74.0060)) < 0.5:
        location_name = "New York"
    elif abs(lat - 35.6762) < 0.5 and abs(lon - 139.6503) < 0.5:
        location_name = "Tokyo"
    elif abs(lat - 48.8566) < 0.5 and abs(lon - 2.3522) < 0.5:
        location_name = "Paris"
    elif abs(lat - (-33.8688)) < 0.5 and abs(lon - 151.2093) < 0.5:
        location_name = "Sydney"
    
    return location_name
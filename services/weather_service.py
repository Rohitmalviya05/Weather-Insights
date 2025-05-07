"""
Weather service for fetching weather data from OpenWeatherMap API.
"""

import os
import logging
import json
import requests
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# API Key from environment variable
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
if not OPENWEATHER_API_KEY:
    logger.warning("OpenWeather API key is not set! Weather data will be mocked.")

# Base URLs for OpenWeatherMap API
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
GEOCODING_URL = "https://api.openweathermap.org/geo/1.0/direct"
REVERSE_GEOCODING_URL = "https://api.openweathermap.org/geo/1.0/reverse"


def get_weather_for_location(lat, lon, units="metric"):
    """
    Get current weather data for a location.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        units (str): Units (metric, imperial, standard)
        
    Returns:
        dict: Weather data
    """
    if not OPENWEATHER_API_KEY:
        logger.warning("Using mock weather data as API key is not set")
        return get_mock_current_weather(lat, lon, units)
    
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": units
        }
        
        response = requests.get(CURRENT_WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Process data to match our desired format
        result = {
            "success": True,
            "location": {
                "name": data.get("name", "Unknown Location"),
                "country": data.get("sys", {}).get("country", ""),
                "lat": lat,
                "lon": lon,
                "timezone": data.get("timezone", 0)
            },
            "current": {
                "dt": data.get("dt", 0),
                "sunrise": data.get("sys", {}).get("sunrise", 0),
                "sunset": data.get("sys", {}).get("sunset", 0),
                "temp": data.get("main", {}).get("temp", 0),
                "feels_like": data.get("main", {}).get("feels_like", 0),
                "pressure": data.get("main", {}).get("pressure", 0),
                "humidity": data.get("main", {}).get("humidity", 0),
                "visibility": data.get("visibility", 0),
                "wind_speed": data.get("wind", {}).get("speed", 0),
                "wind_deg": data.get("wind", {}).get("deg", 0),
                "clouds": data.get("clouds", {}).get("all", 0),
                "weather": {
                    "id": data.get("weather", [{}])[0].get("id", 0),
                    "main": data.get("weather", [{}])[0].get("main", "Unknown"),
                    "description": data.get("weather", [{}])[0].get("description", "Unknown"),
                    "icon": data.get("weather", [{}])[0].get("icon", "01d")
                }
            }
        }
        
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return {
            "success": False,
            "message": "Unable to fetch weather data. Please try again later.",
            "error": str(e)
        }


def get_forecast_for_location(lat, lon, units="metric", days=7):
    """
    Get weather forecast for a location.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        units (str): Units (metric, imperial, standard)
        days (int): Number of days to forecast
        
    Returns:
        dict: Forecast data
    """
    if not OPENWEATHER_API_KEY:
        logger.warning("Using mock forecast data as API key is not set")
        return get_mock_forecast(lat, lon, units, days)
    
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": units,
            "cnt": min(days * 8, 40)  # OpenWeatherMap allows max 40 time steps (5 days)
        }
        
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Process forecast data
        result = {
            "success": True,
            "location": {
                "name": data.get("city", {}).get("name", "Unknown Location"),
                "country": data.get("city", {}).get("country", ""),
                "lat": data.get("city", {}).get("coord", {}).get("lat", lat),
                "lon": data.get("city", {}).get("coord", {}).get("lon", lon),
                "timezone": data.get("city", {}).get("timezone", 0)
            },
            "forecast": []
        }
        
        # Group by day for daily forecast
        forecast_by_day = {}
        for item in data.get("list", []):
            dt = datetime.fromtimestamp(item.get("dt", 0))
            day_key = dt.strftime("%Y-%m-%d")
            
            if day_key not in forecast_by_day:
                forecast_by_day[day_key] = {
                    "dt": dt.timestamp(),
                    "day": dt.strftime("%a"),
                    "date": day_key,
                    "temp_min": float('inf'),
                    "temp_max": float('-inf'),
                    "temps": [],
                    "humidity_avg": 0,
                    "humidity_values": [],
                    "weather_ids": [],
                    "weather_descriptions": [],
                    "icons": [],
                    "rain_chance": 0,
                    "wind_speed_avg": 0,
                    "wind_speed_values": []
                }
            
            # Update day data
            day_data = forecast_by_day[day_key]
            temp = item.get("main", {}).get("temp", 0)
            day_data["temp_min"] = min(day_data["temp_min"], temp)
            day_data["temp_max"] = max(day_data["temp_max"], temp)
            day_data["temps"].append(temp)
            
            humidity = item.get("main", {}).get("humidity", 0)
            day_data["humidity_values"].append(humidity)
            
            weather_id = item.get("weather", [{}])[0].get("id", 0)
            day_data["weather_ids"].append(weather_id)
            
            weather_desc = item.get("weather", [{}])[0].get("description", "Unknown")
            day_data["weather_descriptions"].append(weather_desc)
            
            icon = item.get("weather", [{}])[0].get("icon", "01d")
            day_data["icons"].append(icon)
            
            rain_chance = item.get("pop", 0) * 100  # Probability of precipitation
            day_data["rain_chance"] = max(day_data["rain_chance"], rain_chance)
            
            wind_speed = item.get("wind", {}).get("speed", 0)
            day_data["wind_speed_values"].append(wind_speed)
        
        # Calculate averages and determine most common weather
        for day_key, day_data in forecast_by_day.items():
            # Average temperature
            day_data["temp_avg"] = sum(day_data["temps"]) / len(day_data["temps"]) if day_data["temps"] else 0
            
            # Average humidity
            day_data["humidity_avg"] = sum(day_data["humidity_values"]) / len(day_data["humidity_values"]) if day_data["humidity_values"] else 0
            
            # Average wind speed
            day_data["wind_speed_avg"] = sum(day_data["wind_speed_values"]) / len(day_data["wind_speed_values"]) if day_data["wind_speed_values"] else 0
            
            # Most common weather condition
            if day_data["weather_ids"]:
                # Count occurrences of each weather id
                id_counts = {}
                for weather_id in day_data["weather_ids"]:
                    id_counts[weather_id] = id_counts.get(weather_id, 0) + 1
                
                # Get most common
                most_common_id = max(id_counts.items(), key=lambda x: x[1])[0]
                idx = day_data["weather_ids"].index(most_common_id)
                
                day_data["weather"] = {
                    "id": most_common_id,
                    "description": day_data["weather_descriptions"][idx],
                    "icon": day_data["icons"][idx]
                }
            else:
                day_data["weather"] = {
                    "id": 800,
                    "description": "Clear sky",
                    "icon": "01d"
                }
            
            # Clean up intermediate data
            del day_data["temps"]
            del day_data["humidity_values"]
            del day_data["weather_ids"]
            del day_data["weather_descriptions"]
            del day_data["icons"]
            del day_data["wind_speed_values"]
            
            # Add to result
            result["forecast"].append(day_data)
        
        # Sort by date
        result["forecast"].sort(key=lambda x: x["date"])
        
        # Limit to requested number of days
        result["forecast"] = result["forecast"][:days]
        
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching forecast data: {e}")
        return {
            "success": False,
            "message": "Unable to fetch forecast data. Please try again later.",
            "error": str(e)
        }


def geocode_location(location_name, limit=5):
    """
    Geocode a location name to coordinates.
    
    Args:
        location_name (str): Location name to geocode
        limit (int): Maximum number of results
        
    Returns:
        dict: Geocoding results
    """
    if not OPENWEATHER_API_KEY:
        logger.warning("Using mock geocoding data as API key is not set")
        return get_mock_geocoding(location_name)
    
    try:
        params = {
            "q": location_name,
            "limit": limit,
            "appid": OPENWEATHER_API_KEY
        }
        
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Process geocoding data
        result = {
            "success": True,
            "results": []
        }
        
        for location in data:
            result["results"].append({
                "name": location.get("name", "Unknown"),
                "country": location.get("country", ""),
                "state": location.get("state", ""),
                "lat": location.get("lat", 0),
                "lon": location.get("lon", 0)
            })
        
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Error geocoding location: {e}")
        return {
            "success": False,
            "message": "Unable to geocode location. Please try again later.",
            "error": str(e)
        }


def reverse_geocode(lat, lon, limit=1):
    """
    Reverse geocode coordinates to location name.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        limit (int): Maximum number of results
        
    Returns:
        dict: Reverse geocoding results
    """
    if not OPENWEATHER_API_KEY:
        logger.warning("Using mock reverse geocoding data as API key is not set")
        return get_mock_reverse_geocoding(lat, lon)
    
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "limit": limit,
            "appid": OPENWEATHER_API_KEY
        }
        
        response = requests.get(REVERSE_GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Process reverse geocoding data
        result = {
            "success": True,
            "results": []
        }
        
        for location in data:
            result["results"].append({
                "name": location.get("name", "Unknown"),
                "country": location.get("country", ""),
                "state": location.get("state", ""),
                "lat": location.get("lat", 0),
                "lon": location.get("lon", 0)
            })
        
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Error reverse geocoding: {e}")
        return {
            "success": False,
            "message": "Unable to reverse geocode. Please try again later.",
            "error": str(e)
        }


# Mock data generators for development/testing without API key
def get_mock_current_weather(lat, lon, units="metric"):
    """
    Generate mock current weather data for development/testing.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        units (str): Units (metric, imperial, standard)
        
    Returns:
        dict: Mock weather data
    """
    # Determine location name based on coordinates (very rough approximation)
    location_name = "London"
    country = "GB"
    
    if lat > 40 and lon < -70:
        location_name = "New York"
        country = "US"
    elif lat > 35 and lat < 36 and lon > 139 and lon < 140:
        location_name = "Tokyo"
        country = "JP"
    
    # Generate mock data
    current_time = int(datetime.now().timestamp())
    sunrise = int((datetime.now().replace(hour=6, minute=0, second=0)).timestamp())
    sunset = int((datetime.now().replace(hour=20, minute=0, second=0)).timestamp())
    
    temp = 22
    feels_like = 23
    if units == "imperial":
        temp = 72
        feels_like = 74
    
    return {
        "success": True,
        "location": {
            "name": location_name,
            "country": country,
            "lat": lat,
            "lon": lon,
            "timezone": 0
        },
        "current": {
            "dt": current_time,
            "sunrise": sunrise,
            "sunset": sunset,
            "temp": temp,
            "feels_like": feels_like,
            "pressure": 1015,
            "humidity": 65,
            "visibility": 10000,
            "wind_speed": 4.5,
            "wind_deg": 270,
            "clouds": 40,
            "weather": {
                "id": 801,
                "main": "Clouds",
                "description": "few clouds",
                "icon": "02d"
            }
        }
    }


def get_mock_forecast(lat, lon, units="metric", days=7):
    """
    Generate mock forecast data for development/testing.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        units (str): Units (metric, imperial, standard)
        days (int): Number of days to forecast
        
    Returns:
        dict: Mock forecast data
    """
    # Determine location name based on coordinates (very rough approximation)
    location_name = "London"
    country = "GB"
    
    if lat > 40 and lon < -70:
        location_name = "New York"
        country = "US"
    elif lat > 35 and lat < 36 and lon > 139 and lon < 140:
        location_name = "Tokyo"
        country = "JP"
    
    # Generate mock forecast
    forecast = []
    base_temp = 22 if units == "metric" else 72
    humidity_base = 65
    wind_speed_base = 4.5
    
    # Weather patterns to create variation
    weather_patterns = [
        {"id": 800, "description": "clear sky", "icon": "01d"},
        {"id": 801, "description": "few clouds", "icon": "02d"},
        {"id": 802, "description": "scattered clouds", "icon": "03d"},
        {"id": 500, "description": "light rain", "icon": "10d"},
        {"id": 501, "description": "moderate rain", "icon": "10d"}
    ]
    
    current_date = datetime.now()
    
    for i in range(days):
        day_date = current_date + timedelta(days=i)
        
        # Create some variation in temperatures
        day_temp_variation = (i % 5) - 2  # -2 to 2 range
        
        # Alternate between weather patterns
        weather_index = i % len(weather_patterns)
        weather = weather_patterns[weather_index]
        
        # Rain chance higher for rain weather patterns
        rain_chance = 10
        if weather["id"] >= 500 and weather["id"] < 600:
            rain_chance = 70
        
        forecast.append({
            "dt": int(day_date.timestamp()),
            "day": day_date.strftime("%a"),
            "date": day_date.strftime("%Y-%m-%d"),
            "temp_min": base_temp - 2 + day_temp_variation,
            "temp_max": base_temp + 5 + day_temp_variation,
            "temp_avg": base_temp + 1.5 + day_temp_variation,
            "humidity_avg": humidity_base + (i % 10),
            "wind_speed_avg": wind_speed_base + (i % 3),
            "weather": weather,
            "rain_chance": rain_chance
        })
    
    return {
        "success": True,
        "location": {
            "name": location_name,
            "country": country,
            "lat": lat,
            "lon": lon,
            "timezone": 0
        },
        "forecast": forecast
    }


def get_mock_geocoding(location_name):
    """
    Generate mock geocoding data for development/testing.
    
    Args:
        location_name (str): Location name to geocode
        
    Returns:
        dict: Mock geocoding results
    """
    # Simple mapping for common cities
    locations = {
        "london": [{"name": "London", "country": "GB", "state": "", "lat": 51.5074, "lon": -0.1278}],
        "new york": [{"name": "New York", "country": "US", "state": "New York", "lat": 40.7128, "lon": -74.0060}],
        "tokyo": [{"name": "Tokyo", "country": "JP", "state": "", "lat": 35.6762, "lon": 139.6503}],
        "paris": [{"name": "Paris", "country": "FR", "state": "", "lat": 48.8566, "lon": 2.3522}],
        "sydney": [{"name": "Sydney", "country": "AU", "state": "New South Wales", "lat": -33.8688, "lon": 151.2093}]
    }
    
    # Check if we have a mock for this location
    lookup_name = location_name.lower()
    
    if lookup_name in locations:
        return {
            "success": True,
            "results": locations[lookup_name]
        }
    
    # Default fallback
    return {
        "success": True,
        "results": [
            {"name": location_name.title(), "country": "US", "state": "", "lat": 40.7128, "lon": -74.0060}
        ]
    }


def get_mock_reverse_geocoding(lat, lon):
    """
    Generate mock reverse geocoding data for development/testing.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        
    Returns:
        dict: Mock reverse geocoding results
    """
    # Very simple approximation
    result = {
        "success": True,
        "results": [
            {"name": "Unknown Location", "country": "US", "state": "", "lat": lat, "lon": lon}
        ]
    }
    
    # Check for some known locations
    if abs(lat - 51.5074) < 0.5 and abs(lon - (-0.1278)) < 0.5:
        result["results"][0] = {"name": "London", "country": "GB", "state": "", "lat": 51.5074, "lon": -0.1278}
    elif abs(lat - 40.7128) < 0.5 and abs(lon - (-74.0060)) < 0.5:
        result["results"][0] = {"name": "New York", "country": "US", "state": "New York", "lat": 40.7128, "lon": -74.0060}
    elif abs(lat - 35.6762) < 0.5 and abs(lon - 139.6503) < 0.5:
        result["results"][0] = {"name": "Tokyo", "country": "JP", "state": "", "lat": 35.6762, "lon": 139.6503}
    
    return result
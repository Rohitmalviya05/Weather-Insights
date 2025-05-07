import math
import random
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Any, Tuple, Optional

from services.weather_service import get_weather_by_coordinates, get_forecast_by_coordinates

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_hyper_local_forecast(lat: float, lon: float) -> Dict[str, Any]:
    """
    Get hyper-localized weather forecast with additional details
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        dict: Enriched weather forecast
    """
    try:
        # Get basic weather data
        current = get_weather_by_coordinates(lat, lon)
        forecast = get_forecast_by_coordinates(lat, lon)
        
        if "error" in current or "error" in forecast:
            error_msg = current.get("error") or forecast.get("error")
            logger.error(f"Error getting data for hyper-local forecast: {error_msg}")
            return {"error": error_msg}
        
        # Calculate additional data
        uv_index = calculate_uv_index(current)
        air_quality = calculate_air_quality(current)
        pollen_level = calculate_pollen_level(current)
        precipitation_chance = calculate_precipitation_chance(current)
        
        # Process the forecast data into a more user-friendly format
        processed_forecast = process_forecast_data(forecast)
        
        # Get neighborhood-level adjustments based on terrain, buildings, etc.
        neighborhood_adjustments = calculate_micro_climate_adjustments(lat, lon, current)
        
        # Combine all data
        return {
            "current": current,
            "uv_index": uv_index,
            "air_quality": air_quality,
            "pollen_level": pollen_level,
            "precipitation_chance": precipitation_chance,
            "forecast": processed_forecast,
            "micro_climate": neighborhood_adjustments,
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in hyper-local forecast: {str(e)}")
        return {"error": str(e)}


def get_health_alerts(lat: float, lon: float, age_group: str = 'adult', 
                     conditions: List[str] = None) -> Dict[str, Any]:
    """
    Get health-related weather alerts and recommendations
    
    Args:
        lat: Latitude
        lon: Longitude
        age_group: Age group (child, adult, senior)
        conditions: List of health conditions to check for
        
    Returns:
        dict: Health alerts and recommendations
    """
    try:
        # Get current weather data
        current = get_weather_by_coordinates(lat, lon)
        forecast = get_forecast_by_coordinates(lat, lon)
        
        if "error" in current or "error" in forecast:
            error_msg = current.get("error") or forecast.get("error")
            logger.error(f"Error getting data for health alerts: {error_msg}")
            return {"error": error_msg}
        
        # Calculate health-related indices
        uv_index = calculate_uv_index(current)
        air_quality = calculate_air_quality(current)
        pollen_level = calculate_pollen_level(current)
        
        # Default to empty list if conditions is None
        if conditions is None:
            conditions = []
        
        # Generate alerts based on conditions and weather
        alerts = generate_health_alerts(current, forecast, age_group, conditions, 
                                       uv_index, air_quality, pollen_level)
        
        # Generate recommendations
        recommendations = generate_health_recommendations(alerts, age_group, conditions)
        
        return {
            "current_weather": {
                "temp": current.get("main", {}).get("temp"),
                "humidity": current.get("main", {}).get("humidity"),
                "pressure": current.get("main", {}).get("pressure"),
                "wind_speed": current.get("wind", {}).get("speed"),
                "weather": current.get("weather", [{}])[0].get("main"),
                "description": current.get("weather", [{}])[0].get("description")
            },
            "health_indices": {
                "uv_index": uv_index,
                "air_quality": air_quality,
                "pollen_level": pollen_level
            },
            "alerts": alerts,
            "recommendations": recommendations,
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in health alerts: {str(e)}")
        return {"error": str(e)}


def get_clothing_recommendations(lat: float, lon: float, gender: str = 'neutral', 
                               activity: str = 'casual') -> Dict[str, Any]:
    """
    Get clothing recommendations based on weather conditions
    
    Args:
        lat: Latitude
        lon: Longitude
        gender: Gender preference (male, female, neutral)
        activity: Activity type (casual, work, sport, formal)
        
    Returns:
        dict: Clothing recommendations
    """
    try:
        # Get current weather data
        current = get_weather_by_coordinates(lat, lon)
        forecast = get_forecast_by_coordinates(lat, lon)
        
        if "error" in current or "error" in forecast:
            error_msg = current.get("error") or forecast.get("error")
            logger.error(f"Error getting data for clothing recommendations: {error_msg}")
            return {"error": error_msg}
        
        # Get weather parameters
        temp = current.get("main", {}).get("temp")
        feels_like = current.get("main", {}).get("feels_like")
        humidity = current.get("main", {}).get("humidity")
        wind_speed = current.get("wind", {}).get("speed")
        weather_condition = current.get("weather", [{}])[0].get("main", "").lower()
        
        # Calculate chance of precipitation
        precipitation_chance = calculate_precipitation_chance(current)
        
        # Generate clothing recommendations
        clothing = generate_clothing_recommendations(
            temp, feels_like, humidity, wind_speed, 
            weather_condition, precipitation_chance, gender, activity
        )
        
        # Generate accessories recommendations
        accessories = generate_accessories_recommendations(
            temp, weather_condition, precipitation_chance, 
            calculate_uv_index(current), activity
        )
        
        return {
            "current_weather": {
                "temp": temp,
                "feels_like": feels_like,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "weather": current.get("weather", [{}])[0].get("main"),
                "description": current.get("weather", [{}])[0].get("description"),
                "precipitation_chance": precipitation_chance
            },
            "clothing": clothing,
            "accessories": accessories,
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in clothing recommendations: {str(e)}")
        return {"error": str(e)}


def get_historical_trends(lat: float, lon: float) -> Dict[str, Any]:
    """
    Get historical weather trends and comparisons
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        dict: Historical weather data and trends
    """
    try:
        # Get current weather data
        current = get_weather_by_coordinates(lat, lon)
        
        if "error" in current:
            error_msg = current.get("error")
            logger.error(f"Error getting data for historical trends: {error_msg}")
            return {"error": error_msg}
        
        # This would normally use historical weather data from an API or database
        # For now, we'll generate example historical data
        temp = current.get("main", {}).get("temp")
        
        # Generate historical average temperatures (example data)
        historical_temps = generate_historical_temperature_data(temp)
        
        # Generate trends and comparisons
        trends = {
            "this_month_vs_average": round(temp - historical_temps["this_month_avg"], 1),
            "this_year_vs_last_year": round(temp - historical_temps["last_year_same_day"], 1),
            "temp_trend_this_month": "rising" if temp > historical_temps["this_month_avg"] else "falling",
            "notable_records": generate_notable_records(temp, historical_temps)
        }
        
        return {
            "current_temperature": temp,
            "historical_averages": historical_temps,
            "trends": trends,
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in historical trends: {str(e)}")
        return {"error": str(e)}


def get_commute_forecast(start_lat: float, start_lon: float, end_lat: float, end_lon: float,
                       departure_time: str = None) -> Dict[str, Any]:
    """
    Get weather forecast for a commute route
    
    Args:
        start_lat: Starting point latitude
        start_lon: Starting point longitude
        end_lat: Ending point latitude
        end_lon: Ending point longitude
        departure_time: Departure time (ISO format string)
        
    Returns:
        dict: Commute weather forecast
    """
    try:
        # Get weather at starting point
        start_weather = get_weather_by_coordinates(start_lat, start_lon)
        
        # Get weather at ending point
        end_weather = get_weather_by_coordinates(end_lat, end_lon)
        
        if "error" in start_weather or "error" in end_weather:
            error_msg = start_weather.get("error") or end_weather.get("error")
            logger.error(f"Error getting data for commute forecast: {error_msg}")
            return {"error": error_msg}
        
        # Parse departure time or use current time
        if departure_time:
            try:
                departure_dt = datetime.fromisoformat(departure_time)
            except ValueError:
                departure_dt = datetime.now()
        else:
            departure_dt = datetime.now()
        
        # Calculate approximate travel weather (midpoint)
        mid_lat = (start_lat + end_lat) / 2
        mid_lon = (start_lon + end_lon) / 2
        mid_weather = get_weather_by_coordinates(mid_lat, mid_lon)
        
        # Generate commute impact assessment
        impact = generate_commute_impact(start_weather, mid_weather, end_weather)
        
        # Calculate route points for a simplified route
        route_points = generate_route_points(start_lat, start_lon, end_lat, end_lon)
        
        # Get weather for each point to create a route forecast
        route_forecast = []
        for point in route_points:
            point_weather = get_weather_by_coordinates(point["lat"], point["lon"])
            route_forecast.append({
                "location": point,
                "weather": {
                    "temp": point_weather.get("main", {}).get("temp"),
                    "condition": point_weather.get("weather", [{}])[0].get("main"),
                    "description": point_weather.get("weather", [{}])[0].get("description"),
                    "icon": point_weather.get("weather", [{}])[0].get("icon")
                }
            })
        
        return {
            "departure_time": departure_dt.isoformat(),
            "start_point": {
                "lat": start_lat,
                "lon": start_lon,
                "weather": {
                    "temp": start_weather.get("main", {}).get("temp"),
                    "condition": start_weather.get("weather", [{}])[0].get("main"),
                    "description": start_weather.get("weather", [{}])[0].get("description")
                }
            },
            "end_point": {
                "lat": end_lat,
                "lon": end_lon,
                "weather": {
                    "temp": end_weather.get("main", {}).get("temp"),
                    "condition": end_weather.get("weather", [{}])[0].get("main"),
                    "description": end_weather.get("weather", [{}])[0].get("description")
                }
            },
            "route_forecast": route_forecast,
            "impact": impact,
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in commute forecast: {str(e)}")
        return {"error": str(e)}


def get_gardening_advice(lat: float, lon: float) -> Dict[str, Any]:
    """
    Get gardening recommendations based on weather conditions
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        dict: Gardening advice and recommendations
    """
    try:
        # Get current weather data
        current = get_weather_by_coordinates(lat, lon)
        forecast = get_forecast_by_coordinates(lat, lon)
        
        if "error" in current or "error" in forecast:
            error_msg = current.get("error") or forecast.get("error")
            logger.error(f"Error getting data for gardening advice: {error_msg}")
            return {"error": error_msg}
        
        # Get weather parameters
        temp = current.get("main", {}).get("temp")
        humidity = current.get("main", {}).get("humidity")
        wind_speed = current.get("wind", {}).get("speed")
        weather_condition = current.get("weather", [{}])[0].get("main", "").lower()
        
        # Process forecast for gardening activities
        processed_forecast = process_forecast_data(forecast)
        
        # Generate gardening advice
        watering_schedule = generate_watering_schedule(processed_forecast, temp, humidity)
        planting_days = generate_planting_days(processed_forecast)
        harvesting_days = generate_harvesting_days(processed_forecast)
        pest_warnings = generate_pest_warnings(temp, humidity, weather_condition)
        garden_tasks = generate_garden_tasks(current, processed_forecast)
        
        return {
            "current_weather": {
                "temp": temp,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "weather": current.get("weather", [{}])[0].get("main"),
                "description": current.get("weather", [{}])[0].get("description")
            },
            "watering_schedule": watering_schedule,
            "optimal_days": {
                "planting": planting_days,
                "harvesting": harvesting_days
            },
            "pest_warnings": pest_warnings,
            "garden_tasks": garden_tasks,
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in gardening advice: {str(e)}")
        return {"error": str(e)}


def get_trip_planning_data(lat: float, lon: float, start_date: str, end_date: str) -> Dict[str, Any]:
    """
    Get weather-based trip planning data
    
    Args:
        lat: Latitude
        lon: Longitude
        start_date: Trip start date (YYYY-MM-DD)
        end_date: Trip end date (YYYY-MM-DD)
        
    Returns:
        dict: Trip planning data with forecast and recommendations
    """
    try:
        # Get current weather data
        current = get_weather_by_coordinates(lat, lon)
        forecast = get_forecast_by_coordinates(lat, lon)
        
        if "error" in current or "error" in forecast:
            error_msg = current.get("error") or forecast.get("error")
            logger.error(f"Error getting data for trip planning: {error_msg}")
            return {"error": error_msg}
        
        # Parse dates
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError as e:
            return {"error": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"}
        
        # Process forecast data for trip dates
        processed_forecast = process_forecast_data(forecast)
        
        # Filter forecast for trip dates (limited by API to 5 days)
        trip_forecast = []
        for day in processed_forecast:
            forecast_date = datetime.fromtimestamp(day["dt"])
            if start_dt <= forecast_date <= end_dt:
                trip_forecast.append(day)
        
        # Generate packing recommendations
        packing_list = generate_packing_list(trip_forecast)
        
        # Generate activity recommendations
        activities = generate_activity_recommendations(trip_forecast)
        
        # Generate weather risks
        weather_risks = generate_weather_risks(trip_forecast)
        
        # Location information
        location = current.get("name", "Unknown Location")
        
        return {
            "location": location,
            "trip_dates": {
                "start": start_date,
                "end": end_date
            },
            "forecast": trip_forecast,
            "packing_list": packing_list,
            "activities": activities,
            "weather_risks": weather_risks,
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in trip planning data: {str(e)}")
        return {"error": str(e)}


def get_smart_notifications(lat: float, lon: float) -> List[Dict[str, Any]]:
    """
    Get smart weather notifications and alerts
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        list: Smart notifications
    """
    try:
        # Get current weather data
        current = get_weather_by_coordinates(lat, lon)
        forecast = get_forecast_by_coordinates(lat, lon)
        
        if "error" in current or "error" in forecast:
            error_msg = current.get("error") or forecast.get("error")
            logger.error(f"Error getting data for smart notifications: {error_msg}")
            return [{"error": error_msg}]
        
        # Process forecast data
        processed_forecast = process_forecast_data(forecast)
        
        # Generate notifications based on weather patterns
        notifications = []
        
        # Check for temperature changes
        temp_notification = generate_temperature_change_notification(processed_forecast)
        if temp_notification:
            notifications.append(temp_notification)
        
        # Check for precipitation
        precip_notification = generate_precipitation_notification(processed_forecast)
        if precip_notification:
            notifications.append(precip_notification)
        
        # Check for severe weather
        severe_notification = generate_severe_weather_notification(processed_forecast)
        if severe_notification:
            notifications.append(severe_notification)
        
        # Check for ideal conditions for activities
        activity_notification = generate_activity_opportunity_notification(processed_forecast)
        if activity_notification:
            notifications.append(activity_notification)
        
        # Check for dry spells
        dry_spell_notification = generate_dry_spell_notification(processed_forecast)
        if dry_spell_notification:
            notifications.append(dry_spell_notification)
        
        # Add creation timestamp to each notification
        for notification in notifications:
            notification["created_at"] = datetime.now().isoformat()
        
        return notifications
    except Exception as e:
        logger.error(f"Error in smart notifications: {str(e)}")
        return [{"error": str(e)}]


# Helper functions

def calculate_uv_index(weather_data: Dict[str, Any]) -> int:
    """Calculate UV index based on weather data"""
    # In reality, this would use actual UV data from an API
    # Here we'll make an educated guess based on weather conditions
    clouds = weather_data.get("clouds", {}).get("all", 0)
    weather_id = weather_data.get("weather", [{}])[0].get("id", 800)
    
    # Base UV value (higher for clear skies)
    base_uv = 8 if weather_id == 800 else 6
    
    # Adjust for cloud cover
    cloud_factor = 1 - (clouds / 100) * 0.7
    
    # Final UV index (1-11 scale)
    uv_index = round(base_uv * cloud_factor)
    
    # Ensure it's within valid range
    return max(1, min(11, uv_index))


def calculate_air_quality(weather_data: Dict[str, Any]) -> int:
    """Calculate air quality index based on weather data"""
    # In reality, this would use actual air quality data from an API
    # Here we'll make an educated guess based on weather conditions
    weather_id = weather_data.get("weather", [{}])[0].get("id", 800)
    wind_speed = weather_data.get("wind", {}).get("speed", 5)
    
    # Base AQI (1-5 scale, lower is better)
    # Assume better air quality with rain and snow, worse with dust/fog
    if weather_id >= 200 and weather_id < 600:  # Thunderstorm, drizzle, rain, snow
        base_aqi = 2
    elif weather_id >= 700 and weather_id < 800:  # Atmosphere (fog, dust, etc.)
        base_aqi = 4
    else:  # Clear or clouds
        base_aqi = 3
    
    # Adjust for wind speed (stronger wind usually means better air quality)
    wind_factor = max(0, 1 - (wind_speed / 10))
    
    # Final AQI (1-5 scale, 1=good, 5=very poor)
    return max(1, min(5, round(base_aqi * (1 + wind_factor * 0.5))))


def calculate_pollen_level(weather_data: Dict[str, Any]) -> int:
    """Calculate pollen level based on weather data"""
    # In reality, this would use actual pollen data from an API
    # Here we'll make an educated guess based on weather conditions
    weather_id = weather_data.get("weather", [{}])[0].get("id", 800)
    humidity = weather_data.get("main", {}).get("humidity", 50)
    
    # Base pollen level (1-5 scale)
    # Pollen tends to be lower during rain, higher during dry, clear conditions
    if weather_id >= 200 and weather_id < 600:  # Thunderstorm, drizzle, rain, snow
        base_pollen = 1
    elif weather_id >= 700 and weather_id < 800:  # Atmosphere (fog, dust, etc.)
        base_pollen = 3
    else:  # Clear or clouds
        base_pollen = 4
    
    # Adjust for humidity (very high or very low humidity can reduce pollen)
    humidity_factor = 1
    if humidity < 30 or humidity > 80:
        humidity_factor = 0.7
    
    # Final pollen level (1-5 scale, 1=low, 5=very high)
    return max(1, min(5, round(base_pollen * humidity_factor)))


def calculate_precipitation_chance(weather_data: Dict[str, Any]) -> float:
    """Calculate chance of precipitation based on weather data"""
    # In reality, this would use actual precipitation probability from an API
    # Here we'll make an educated guess based on weather conditions
    weather_id = weather_data.get("weather", [{}])[0].get("id", 800)
    clouds = weather_data.get("clouds", {}).get("all", 0)
    humidity = weather_data.get("main", {}).get("humidity", 50)
    
    # Base precipitation chance
    if weather_id >= 200 and weather_id < 300:  # Thunderstorm
        base_chance = 0.9
    elif weather_id >= 300 and weather_id < 400:  # Drizzle
        base_chance = 0.7
    elif weather_id >= 500 and weather_id < 600:  # Rain
        base_chance = 0.8
    elif weather_id >= 600 and weather_id < 700:  # Snow
        base_chance = 0.8
    elif weather_id >= 700 and weather_id < 800:  # Atmosphere (fog, dust, etc.)
        base_chance = 0.3
    elif weather_id == 800:  # Clear
        base_chance = 0.1
    elif weather_id > 800:  # Clouds
        base_chance = 0.2 + (clouds / 100) * 0.4
    else:
        base_chance = 0.2
    
    # Adjust for humidity (higher humidity increases chance)
    humidity_factor = humidity / 100
    
    # Final precipitation chance (0-1)
    return min(1.0, base_chance * (1 + humidity_factor * 0.5))


def process_forecast_data(forecast_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Process forecast data into daily forecasts"""
    result = []
    
    if "list" not in forecast_data:
        return result
    
    # Group by day
    day_forecasts = {}
    
    for item in forecast_data["list"]:
        dt = item["dt"]
        date = datetime.fromtimestamp(dt).strftime("%Y-%m-%d")
        
        if date not in day_forecasts:
            day_forecasts[date] = []
        
        day_forecasts[date].append(item)
    
    # Process each day
    for date, items in day_forecasts.items():
        if not items:
            continue
        
        # First forecast of the day
        first = items[0]
        
        # Calculate min/max temp and average other values
        temps = [item["main"]["temp"] for item in items]
        min_temp = min(temps)
        max_temp = max(temps)
        
        # Main weather condition (mode)
        weather_conditions = [item["weather"][0]["main"] for item in items]
        main_condition = max(set(weather_conditions), key=weather_conditions.count)
        
        # First weather description & icon for that condition
        description = next((item["weather"][0]["description"] for item in items 
                           if item["weather"][0]["main"] == main_condition), items[0]["weather"][0]["description"])
        icon = next((item["weather"][0]["icon"] for item in items 
                    if item["weather"][0]["main"] == main_condition), items[0]["weather"][0]["icon"])
        
        # Calculate precipitation probability
        pop_values = [item.get("pop", 0) for item in items]
        avg_pop = sum(pop_values) / len(pop_values) if pop_values else 0
        
        # Detailed hourly forecast
        hourly = []
        for item in items:
            hourly.append({
                "dt": item["dt"],
                "time": datetime.fromtimestamp(item["dt"]).strftime("%H:%M"),
                "temp": item["main"]["temp"],
                "feels_like": item["main"]["feels_like"],
                "pressure": item["main"]["pressure"],
                "humidity": item["main"]["humidity"],
                "weather": item["weather"][0]["main"],
                "description": item["weather"][0]["description"],
                "icon": item["weather"][0]["icon"],
                "clouds": item["clouds"]["all"],
                "wind_speed": item["wind"]["speed"],
                "wind_deg": item["wind"]["deg"],
                "pop": item.get("pop", 0)
            })
        
        # Create day summary
        day_summary = {
            "dt": first["dt"],
            "date": date,
            "day_name": datetime.fromtimestamp(first["dt"]).strftime("%A"),
            "min_temp": min_temp,
            "max_temp": max_temp,
            "humidity": sum(item["main"]["humidity"] for item in items) / len(items),
            "pressure": sum(item["main"]["pressure"] for item in items) / len(items),
            "weather": main_condition,
            "description": description,
            "icon": icon,
            "wind_speed": sum(item["wind"]["speed"] for item in items) / len(items),
            "pop": avg_pop,
            "hourly": hourly
        }
        
        result.append(day_summary)
    
    # Sort by date
    result.sort(key=lambda x: x["dt"])
    
    return result


def calculate_micro_climate_adjustments(lat: float, lon: float, weather_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate micro-climate adjustments for hyper-local forecast"""
    # In a real implementation, this would use terrain data, building density, etc.
    # Here we'll create some example adjustments
    
    # Make small random adjustments to simulate neighborhood variations
    temp_adjustment = round(random.uniform(-1.0, 1.0), 1)
    humidity_adjustment = round(random.uniform(-5, 5))
    wind_adjustment = round(random.uniform(-1.0, 1.0), 1)
    
    # Current values
    temp = weather_data.get("main", {}).get("temp", 0)
    humidity = weather_data.get("main", {}).get("humidity", 0)
    wind_speed = weather_data.get("wind", {}).get("speed", 0)
    
    return {
        "temperature": {
            "value": round(temp + temp_adjustment, 1),
            "difference": temp_adjustment,
            "reason": get_microclimate_reason(temp_adjustment, "temperature")
        },
        "humidity": {
            "value": round(humidity + humidity_adjustment),
            "difference": humidity_adjustment,
            "reason": get_microclimate_reason(humidity_adjustment, "humidity")
        },
        "wind_speed": {
            "value": round(wind_speed + wind_adjustment, 1),
            "difference": wind_adjustment,
            "reason": get_microclimate_reason(wind_adjustment, "wind")
        }
    }


def get_microclimate_reason(adjustment: float, factor_type: str) -> str:
    """Get reason for microclimate adjustment"""
    if factor_type == "temperature":
        if adjustment > 0.5:
            return "Urban heat island effect"
        elif adjustment < -0.5:
            return "Proximity to water bodies or green spaces"
        else:
            return "Minimal local variation"
    elif factor_type == "humidity":
        if adjustment > 3:
            return "Proximity to water bodies"
        elif adjustment < -3:
            return "Urban density with less vegetation"
        else:
            return "Minimal local variation"
    elif factor_type == "wind":
        if adjustment > 0.5:
            return "Wind tunnel effect between buildings"
        elif adjustment < -0.5:
            return "Wind sheltered by terrain or structures"
        else:
            return "Minimal local variation"
    else:
        return "Local geographic factors"


def generate_health_alerts(current: Dict[str, Any], forecast: Dict[str, Any], 
                         age_group: str, conditions: List[str],
                         uv_index: int, air_quality: int, pollen_level: int) -> List[Dict[str, Any]]:
    """Generate health alerts based on weather and health conditions"""
    alerts = []
    
    # Current weather values
    temp = current.get("main", {}).get("temp")
    humidity = current.get("main", {}).get("humidity")
    
    # UV Index alert
    if uv_index >= 8:
        alerts.append({
            "type": "uv",
            "level": "high",
            "message": "Very high UV levels. Limit sun exposure between 10am-4pm."
        })
    elif uv_index >= 6:
        alerts.append({
            "type": "uv",
            "level": "moderate",
            "message": "Moderate UV levels. Use sunscreen when outdoors."
        })
    
    # Air Quality alert
    if air_quality >= 4:
        alerts.append({
            "type": "air_quality",
            "level": "poor",
            "message": "Poor air quality. Limit outdoor activity if you experience symptoms."
        })
    
    # Pollen alert
    if pollen_level >= 4:
        alerts.append({
            "type": "pollen",
            "level": "high",
            "message": "High pollen levels. Take preventive medication if allergic."
        })
    
    # Temperature alerts
    if temp >= 32:
        alerts.append({
            "type": "heat",
            "level": "extreme",
            "message": "Extreme heat. Stay hydrated and avoid extended outdoor activity."
        })
    elif temp >= 27:
        alerts.append({
            "type": "heat",
            "level": "high",
            "message": "High temperatures. Take breaks and stay hydrated during outdoor activities."
        })
    elif temp <= 0:
        alerts.append({
            "type": "cold",
            "level": "freezing",
            "message": "Freezing temperatures. Bundle up and limit time outdoors."
        })
    elif temp <= 5:
        alerts.append({
            "type": "cold",
            "level": "cold",
            "message": "Cold temperatures. Dress warmly when outdoors."
        })
    
    # Condition-specific alerts
    for condition in conditions:
        condition = condition.lower()
        
        if condition in ["asthma", "copd", "respiratory"]:
            if air_quality >= 3 or pollen_level >= 3:
                alerts.append({
                    "type": "respiratory",
                    "level": "caution",
                    "message": f"Current conditions may aggravate {condition}. Keep medication accessible."
                })
        
        elif condition in ["heart", "cardiovascular"]:
            if temp >= 30 or temp <= 0:
                alerts.append({
                    "type": "cardiovascular",
                    "level": "caution",
                    "message": f"Extreme temperatures may stress the cardiovascular system. Avoid strenuous activity."
                })
        
        elif condition in ["migraine", "headache"]:
            # Pressure changes often trigger migraines
            alerts.append({
                "type": "migraine",
                "level": "informational",
                "message": "Weather changes may trigger migraines. Consider preventive measures."
            })
        
        elif condition in ["arthritis", "joint pain"]:
            if humidity >= 70 or temp <= 10:
                alerts.append({
                    "type": "joint_pain",
                    "level": "informational",
                    "message": "Current conditions may aggravate joint pain. Consider indoor activities."
                })
    
    # Age-specific alerts
    if age_group == "senior" and (temp >= 28 or temp <= 5):
        alerts.append({
            "type": "age_related",
            "level": "caution",
            "message": "Temperature extremes particularly affect seniors. Take extra precautions."
        })
    elif age_group == "child" and uv_index >= 6:
        alerts.append({
            "type": "age_related",
            "level": "caution",
            "message": "Children's skin is sensitive to UV. Use extra protection."
        })
    
    return alerts


def generate_health_recommendations(alerts: List[Dict[str, Any]], age_group: str, conditions: List[str]) -> List[str]:
    """Generate health recommendations based on alerts"""
    recommendations = []
    
    # Check alert types and generate recommendations
    alert_types = [alert["type"] for alert in alerts]
    
    if "uv" in alert_types:
        recommendations.append("Use SPF 30+ sunscreen and reapply every 2 hours when outdoors")
        recommendations.append("Wear a wide-brimmed hat and UV-blocking sunglasses")
    
    if "air_quality" in alert_types:
        recommendations.append("Keep windows closed during peak pollution hours")
        recommendations.append("Use air purifiers indoors if available")
    
    if "pollen" in alert_types:
        recommendations.append("Take antihistamines before symptoms start if you have allergies")
        recommendations.append("Shower after being outdoors to remove pollen from skin and hair")
    
    if "heat" in alert_types:
        recommendations.append("Drink water regularly, even if not thirsty")
        recommendations.append("Wear lightweight, light-colored, loose-fitting clothing")
        if age_group == "senior":
            recommendations.append("Check on elderly friends and relatives during heat waves")
    
    if "cold" in alert_types:
        recommendations.append("Dress in layers with waterproof outer layer if precipitation expected")
        recommendations.append("Keep extremities covered with gloves, warm socks, and a hat")
    
    # Add condition-specific recommendations
    for condition in conditions:
        condition = condition.lower()
        
        if condition in ["asthma", "copd", "respiratory"]:
            if "air_quality" in alert_types or "pollen" in alert_types:
                recommendations.append("Carry rescue medication at all times")
                recommendations.append("Consider wearing a mask outdoors on high pollution days")
        
        elif condition in ["heart", "cardiovascular"]:
            if "heat" in alert_types or "cold" in alert_types:
                recommendations.append("Avoid sudden exertion in extreme temperatures")
                recommendations.append("Schedule outdoor activities during moderate temperature periods")
        
        elif condition in ["migraine", "headache"]:
            recommendations.append("Track weather changes and take preventive medication if needed")
            recommendations.append("Stay hydrated to help prevent weather-related headaches")
        
        elif condition in ["arthritis", "joint pain"]:
            recommendations.append("Apply heat therapy on cold days to relieve joint stiffness")
            recommendations.append("Consider indoor exercises during extreme weather")
    
    # Age-specific recommendations
    if age_group == "senior":
        recommendations.append("Stay hydrated as older adults have a decreased ability to sense thirst")
        if "cold" in alert_types:
            recommendations.append("Use extra layers as seniors are more sensitive to cold")
    elif age_group == "child":
        if "uv" in alert_types:
            recommendations.append("Children need extra UV protection - use child-safe sunscreen")
        if "heat" in alert_types:
            recommendations.append("Children dehydrate more quickly - encourage regular water breaks")
    
    return sorted(list(set(recommendations)))  # Remove duplicates


def generate_clothing_recommendations(temp: float, feels_like: float, humidity: int, 
                                    wind_speed: float, weather_condition: str, 
                                    precipitation_chance: float, gender: str, 
                                    activity: str) -> List[Dict[str, str]]:
    """Generate clothing recommendations based on weather conditions"""
    clothing = []
    
    # Adjust for wind chill and humidity
    effective_temp = feels_like
    
    # Base clothing by temperature range
    if effective_temp >= 30:  # Very hot
        if gender == "male":
            clothing.append({"item": "T-shirt", "type": "top"})
            clothing.append({"item": "Shorts", "type": "bottom"})
        elif gender == "female":
            clothing.append({"item": "Light top", "type": "top"})
            clothing.append({"item": "Shorts or skirt", "type": "bottom"})
        else:  # neutral
            clothing.append({"item": "Light top", "type": "top"})
            clothing.append({"item": "Shorts", "type": "bottom"})
    
    elif effective_temp >= 25:  # Hot
        if gender == "male":
            clothing.append({"item": "T-shirt", "type": "top"})
            clothing.append({"item": "Shorts or light pants", "type": "bottom"})
        elif gender == "female":
            clothing.append({"item": "Light top or t-shirt", "type": "top"})
            clothing.append({"item": "Shorts, skirt, or light pants", "type": "bottom"})
        else:  # neutral
            clothing.append({"item": "T-shirt", "type": "top"})
            clothing.append({"item": "Shorts or light pants", "type": "bottom"})
    
    elif effective_temp >= 20:  # Warm
        if gender == "male":
            clothing.append({"item": "Light shirt", "type": "top"})
            clothing.append({"item": "Light pants", "type": "bottom"})
        elif gender == "female":
            clothing.append({"item": "Light blouse or t-shirt", "type": "top"})
            clothing.append({"item": "Light pants or casual skirt", "type": "bottom"})
        else:  # neutral
            clothing.append({"item": "Light shirt", "type": "top"})
            clothing.append({"item": "Light pants", "type": "bottom"})
    
    elif effective_temp >= 15:  # Mild
        if gender == "male":
            clothing.append({"item": "Long-sleeved shirt", "type": "top"})
            clothing.append({"item": "Pants", "type": "bottom"})
        elif gender == "female":
            clothing.append({"item": "Long-sleeved top", "type": "top"})
            clothing.append({"item": "Pants or long skirt", "type": "bottom"})
        else:  # neutral
            clothing.append({"item": "Long-sleeved shirt", "type": "top"})
            clothing.append({"item": "Pants", "type": "bottom"})
    
    elif effective_temp >= 10:  # Cool
        if gender == "male":
            clothing.append({"item": "Long-sleeved shirt", "type": "top"})
            clothing.append({"item": "Light sweater", "type": "mid_layer"})
            clothing.append({"item": "Pants", "type": "bottom"})
        elif gender == "female":
            clothing.append({"item": "Long-sleeved top", "type": "top"})
            clothing.append({"item": "Light sweater or cardigan", "type": "mid_layer"})
            clothing.append({"item": "Pants or long skirt", "type": "bottom"})
        else:  # neutral
            clothing.append({"item": "Long-sleeved shirt", "type": "top"})
            clothing.append({"item": "Light sweater", "type": "mid_layer"})
            clothing.append({"item": "Pants", "type": "bottom"})
    
    elif effective_temp >= 5:  # Chilly
        if gender == "male":
            clothing.append({"item": "Long-sleeved shirt", "type": "top"})
            clothing.append({"item": "Sweater", "type": "mid_layer"})
            clothing.append({"item": "Light jacket", "type": "outer_layer"})
            clothing.append({"item": "Pants", "type": "bottom"})
        elif gender == "female":
            clothing.append({"item": "Long-sleeved top", "type": "top"})
            clothing.append({"item": "Sweater or cardigan", "type": "mid_layer"})
            clothing.append({"item": "Light jacket", "type": "outer_layer"})
            clothing.append({"item": "Pants or jeans", "type": "bottom"})
        else:  # neutral
            clothing.append({"item": "Long-sleeved shirt", "type": "top"})
            clothing.append({"item": "Sweater", "type": "mid_layer"})
            clothing.append({"item": "Light jacket", "type": "outer_layer"})
            clothing.append({"item": "Pants", "type": "bottom"})
    
    elif effective_temp >= 0:  # Cold
        if gender == "male":
            clothing.append({"item": "Thermal undershirt", "type": "base_layer"})
            clothing.append({"item": "Long-sleeved shirt", "type": "top"})
            clothing.append({"item": "Sweater", "type": "mid_layer"})
            clothing.append({"item": "Jacket", "type": "outer_layer"})
            clothing.append({"item": "Pants", "type": "bottom"})
        elif gender == "female":
            clothing.append({"item": "Thermal top", "type": "base_layer"})
            clothing.append({"item": "Long-sleeved top", "type": "top"})
            clothing.append({"item": "Sweater", "type": "mid_layer"})
            clothing.append({"item": "Jacket", "type": "outer_layer"})
            clothing.append({"item": "Pants or jeans", "type": "bottom"})
        else:  # neutral
            clothing.append({"item": "Thermal top", "type": "base_layer"})
            clothing.append({"item": "Long-sleeved shirt", "type": "top"})
            clothing.append({"item": "Sweater", "type": "mid_layer"})
            clothing.append({"item": "Jacket", "type": "outer_layer"})
            clothing.append({"item": "Pants", "type": "bottom"})
    
    else:  # Very cold (below 0)
        if gender == "male":
            clothing.append({"item": "Thermal underwear", "type": "base_layer"})
            clothing.append({"item": "Long-sleeved shirt", "type": "top"})
            clothing.append({"item": "Heavy sweater", "type": "mid_layer"})
            clothing.append({"item": "Winter coat", "type": "outer_layer"})
            clothing.append({"item": "Insulated pants", "type": "bottom"})
        elif gender == "female":
            clothing.append({"item": "Thermal underwear", "type": "base_layer"})
            clothing.append({"item": "Long-sleeved top", "type": "top"})
            clothing.append({"item": "Heavy sweater", "type": "mid_layer"})
            clothing.append({"item": "Winter coat", "type": "outer_layer"})
            clothing.append({"item": "Insulated pants", "type": "bottom"})
        else:  # neutral
            clothing.append({"item": "Thermal underwear", "type": "base_layer"})
            clothing.append({"item": "Long-sleeved shirt", "type": "top"})
            clothing.append({"item": "Heavy sweater", "type": "mid_layer"})
            clothing.append({"item": "Winter coat", "type": "outer_layer"})
            clothing.append({"item": "Insulated pants", "type": "bottom"})
    
    # Adjustments for rain
    if weather_condition in ["rain", "drizzle", "thunderstorm"] or precipitation_chance > 0.4:
        # Replace jacket with rain jacket if already present
        for item in clothing:
            if item["type"] == "outer_layer":
                item["item"] = "Waterproof " + item["item"].lower()
                break
        else:
            # Add rain jacket if no outer layer
            clothing.append({"item": "Rain jacket", "type": "outer_layer"})
    
    # Adjustments for wind
    if wind_speed > 5 and "outer_layer" not in [item["type"] for item in clothing]:
        if effective_temp < 15:
            clothing.append({"item": "Windbreaker", "type": "outer_layer"})
    
    # Adjustments for activity
    if activity == "sport":
        # Replace regular clothing with sport-specific items
        for item in clothing:
            if item["type"] == "top":
                item["item"] = "Moisture-wicking " + item["item"].lower()
            elif item["type"] == "bottom" and effective_temp > 10:
                item["item"] = "Athletic shorts" if effective_temp > 20 else "Athletic pants"
            elif item["type"] == "bottom":
                item["item"] = "Athletic pants"
    
    elif activity == "formal":
        # Replace casual clothing with formal items
        for item in clothing:
            if item["type"] == "top":
                item["item"] = "Dress shirt" if gender != "female" else "Blouse"
            elif item["type"] == "bottom":
                item["item"] = "Dress pants" if gender != "female" else "Dress pants or skirt"
        
        # Add formal outer layer if needed
        if effective_temp < 15 and "outer_layer" not in [item["type"] for item in clothing]:
            clothing.append({"item": "Blazer", "type": "outer_layer"})
    
    elif activity == "work":
        # Adjust for work environment
        for item in clothing:
            if item["type"] == "top":
                item["item"] = "Collared shirt" if gender != "female" else "Blouse or collared shirt"
    
    return clothing


def generate_accessories_recommendations(temp: float, weather_condition: str, 
                                       precipitation_chance: float, uv_index: int,
                                       activity: str) -> List[Dict[str, str]]:
    """Generate accessories recommendations based on weather conditions"""
    accessories = []
    
    # Rain accessories
    if weather_condition in ["rain", "drizzle", "thunderstorm"] or precipitation_chance > 0.4:
        accessories.append({"item": "Umbrella", "reason": "Rain protection"})
        accessories.append({"item": "Waterproof footwear", "reason": "Keep feet dry"})
    
    # Cold weather accessories
    if temp <= 10:
        accessories.append({"item": "Scarf", "reason": "Neck warmth"})
    if temp <= 5:
        accessories.append({"item": "Gloves", "reason": "Hand warmth"})
        accessories.append({"item": "Hat or beanie", "reason": "Head warmth"})
    if temp <= 0:
        accessories.append({"item": "Thermal socks", "reason": "Foot warmth"})
    
    # Hot weather accessories
    if temp >= 25:
        accessories.append({"item": "Water bottle", "reason": "Stay hydrated"})
    
    # Sun protection
    if uv_index >= 3:
        accessories.append({"item": "Sunglasses", "reason": "UV eye protection"})
        accessories.append({"item": "Sunscreen", "reason": "Skin protection"})
    if uv_index >= 6:
        accessories.append({"item": "Hat with brim", "reason": "Shade for face and neck"})
    
    # Activity-specific accessories
    if activity == "sport":
        accessories.append({"item": "Athletic socks", "reason": "Comfort during activity"})
        if temp >= 20:
            accessories.append({"item": "Sport water bottle", "reason": "Hydration during activity"})
    
    elif activity == "formal":
        if weather_condition in ["rain", "drizzle"]:
            accessories.append({"item": "Formal umbrella", "reason": "Rain protection"})
    
    return accessories


def generate_historical_temperature_data(current_temp: float) -> Dict[str, float]:
    """Generate historical temperature data for comparison"""
    # This would normally come from a historical weather API or database
    # For now, we'll generate reasonable values based on the current temperature
    
    # Add some variation around the current temperature
    last_week_avg = round(current_temp + random.uniform(-2, 2), 1)
    last_month_avg = round(current_temp + random.uniform(-3, 3), 1)
    last_year_same_day = round(current_temp + random.uniform(-5, 5), 1)
    
    # Historical averages (would normally be from real data)
    this_month_avg = round(current_temp - random.uniform(0, 3), 1)  # Historical average usually lower than current
    year_avg = round((current_temp + this_month_avg) / 2, 1)
    ten_year_avg = round(this_month_avg - random.uniform(0, 1), 1)  # 10-year average typically lower due to warming
    
    return {
        "last_week_avg": last_week_avg,
        "last_month_avg": last_month_avg,
        "last_year_same_day": last_year_same_day,
        "this_month_avg": this_month_avg,
        "year_avg": year_avg,
        "ten_year_avg": ten_year_avg
    }


def generate_notable_records(current_temp: float, historical_data: Dict[str, float]) -> List[str]:
    """Generate notable weather records based on current and historical data"""
    records = []
    
    # Variations from averages
    month_diff = current_temp - historical_data["this_month_avg"]
    if abs(month_diff) > 5:
        direction = "above" if month_diff > 0 else "below"
        records.append(f"Temperature is {abs(round(month_diff, 1))}°C {direction} the monthly average")
    
    # Compare to 10-year average
    decade_diff = current_temp - historical_data["ten_year_avg"]
    if decade_diff > 3:
        records.append(f"Currently {round(decade_diff, 1)}°C warmer than the 10-year average")
    
    # Add a record about trends
    if historical_data["last_year_same_day"] < historical_data["ten_year_avg"]:
        records.append("This day has been warming over the past decade")
    
    # Add a seasonal record
    month = datetime.now().month
    if (month >= 3 and month <= 5) or (month >= 9 and month <= 11):  # Spring or Fall
        records.append("Temperature variations are typical for transitional season")
    elif month >= 6 and month <= 8:  # Summer
        if current_temp > 30:
            records.append("Current temperature is in the upper range for this season")
    else:  # Winter
        if current_temp < 0:
            records.append("Current temperature is in the typical winter range")
    
    return records


def generate_commute_impact(start_weather: Dict[str, Any], mid_weather: Dict[str, Any], 
                          end_weather: Dict[str, Any]) -> Dict[str, Any]:
    """Generate commute impact assessment based on weather conditions"""
    # Get relevant weather conditions
    start_condition = start_weather.get("weather", [{}])[0].get("main", "").lower()
    mid_condition = mid_weather.get("weather", [{}])[0].get("main", "").lower()
    end_condition = end_weather.get("weather", [{}])[0].get("main", "").lower()
    
    # Check for precipitation conditions
    precip_conditions = ["rain", "drizzle", "snow", "thunderstorm"]
    has_precip = any(cond in [start_condition, mid_condition, end_condition] for cond in precip_conditions)
    
    # Check for visibility issues
    vis_conditions = ["fog", "mist", "haze", "smoke", "dust", "sand"]
    low_vis = any(cond in [start_condition, mid_condition, end_condition] for cond in vis_conditions)
    
    # Determine severity level
    severity = 0  # 0: minimal, 1: minor, 2: moderate, 3: significant
    
    if has_precip:
        if "thunderstorm" in [start_condition, mid_condition, end_condition]:
            severity = 3
        elif "snow" in [start_condition, mid_condition, end_condition]:
            severity = 2
        else:  # rain, drizzle
            severity = 1
    
    if low_vis:
        severity = max(severity, 2)
    
    # Wind impact
    max_wind = max(
        start_weather.get("wind", {}).get("speed", 0),
        mid_weather.get("wind", {}).get("speed", 0),
        end_weather.get("wind", {}).get("speed", 0)
    )
    
    if max_wind > 10:
        severity = max(severity, 2)
    elif max_wind > 5:
        severity = max(severity, 1)
    
    # Determine delay time based on severity
    delay_minutes = 0
    if severity == 1:
        delay_minutes = random.randint(3, 7)
    elif severity == 2:
        delay_minutes = random.randint(8, 15)
    elif severity == 3:
        delay_minutes = random.randint(15, 30)
    
    # Generate impact message
    impact_msg = ""
    if severity == 0:
        impact_msg = "Good weather conditions. No significant impact on commute."
    elif severity == 1:
        impact_msg = f"Minor weather-related slowdowns possible. Allow {delay_minutes} extra minutes."
    elif severity == 2:
        impact_msg = f"Moderate weather impacts expected. Allow {delay_minutes} extra minutes and use caution."
    else:
        impact_msg = f"Significant weather impacts expected. Allow {delay_minutes}+ extra minutes. Consider alternate routes."
    
    # Weather tips
    tips = []
    if has_precip:
        tips.append("Reduced visibility and slippery conditions possible")
        if "thunderstorm" in [start_condition, mid_condition, end_condition]:
            tips.append("Be alert for flooded areas and potential road closures")
    
    if low_vis:
        tips.append("Use headlights and maintain extra distance between vehicles")
    
    if max_wind > 5:
        tips.append("Be cautious of strong crosswinds, especially on bridges")
    
    return {
        "severity": severity,
        "delay_minutes": delay_minutes,
        "message": impact_msg,
        "tips": tips
    }


def generate_route_points(start_lat: float, start_lon: float, 
                        end_lat: float, end_lon: float, points: int = 5) -> List[Dict[str, float]]:
    """Generate route points between start and end coordinates"""
    route = []
    
    # Add starting point
    route.append({
        "lat": start_lat,
        "lon": start_lon,
        "position": 0
    })
    
    # Generate intermediate points (simple linear interpolation)
    for i in range(1, points - 1):
        progress = i / (points - 1)
        lat = start_lat + (end_lat - start_lat) * progress
        lon = start_lon + (end_lon - start_lon) * progress
        
        # Add slight random variation to simulate a realistic route
        lat_variation = random.uniform(-0.005, 0.005)
        lon_variation = random.uniform(-0.005, 0.005)
        
        route.append({
            "lat": lat + lat_variation,
            "lon": lon + lon_variation,
            "position": progress
        })
    
    # Add ending point
    route.append({
        "lat": end_lat,
        "lon": end_lon,
        "position": 1
    })
    
    return route


def generate_watering_schedule(forecast: List[Dict[str, Any]], temp: float, humidity: int) -> Dict[str, Any]:
    """Generate optimal watering schedule for gardening"""
    # Determine best watering times based on weather patterns
    watering_times = []
    
    # Calculate evapotranspiration risk based on temperature and humidity
    et_risk = "high" if temp > 25 and humidity < 50 else "moderate" if temp > 20 else "low"
    
    # Find days without rain
    rainy_days = []
    dry_days = []
    
    for day in forecast:
        if day.get("pop", 0) > 0.4:  # >40% chance of precipitation
            rainy_days.append(day["date"])
        else:
            dry_days.append(day["date"])
    
    # For today, recommend early morning or evening watering
    today = datetime.now().strftime("%Y-%m-%d")
    if today in dry_days:
        # Early morning (optimal)
        watering_times.append({
            "day": today,
            "time": "06:00-08:00",
            "quality": "excellent",
            "reason": "Low evaporation and good absorption"
        })
        
        # Evening (good alternative)
        watering_times.append({
            "day": today,
            "time": "19:00-21:00",
            "quality": "good",
            "reason": "Lower evaporation but increased disease risk"
        })
    
    # For future dry days
    for day in dry_days:
        if day != today:
            watering_times.append({
                "day": day,
                "time": "06:00-08:00",
                "quality": "excellent",
                "reason": "Low evaporation and good absorption"
            })
    
    # Custom advice based on conditions
    advice = []
    if et_risk == "high":
        advice.append("Water deeply and less frequently to encourage deep root growth")
        advice.append("Consider using mulch to reduce soil moisture evaporation")
    
    if len(rainy_days) >= 2:
        advice.append("Natural rainfall may reduce watering needs on some days")
    
    if humidity < 40:
        advice.append("Consider using a soaker hose or drip irrigation to reduce water waste")
    
    return {
        "watering_times": watering_times,
        "evapotranspiration_risk": et_risk,
        "advice": advice
    }


def generate_planting_days(forecast: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate optimal planting days based on forecast"""
    planting_days = []
    
    for day in forecast:
        # Ideal planting conditions: mild temperatures, low wind, no heavy rain
        temp_good = 10 <= day.get("min_temp", 0) <= 25
        wind_good = day.get("wind_speed", 0) < 5
        rain_good = day.get("pop", 0) < 0.5
        
        if temp_good and wind_good and rain_good:
            quality = "excellent"
        elif temp_good and (wind_good or rain_good):
            quality = "good"
        else:
            quality = "poor"
        
        reasons = []
        if not temp_good:
            if day.get("min_temp", 0) < 10:
                reasons.append("Soil too cold")
            else:
                reasons.append("Too hot for transplanting")
        
        if not wind_good:
            reasons.append("Wind may stress new plants")
        
        if not rain_good:
            reasons.append("Heavy rain may damage seedlings")
        
        planting_days.append({
            "date": day["date"],
            "day_name": day["day_name"],
            "quality": quality,
            "reasons": reasons if reasons else ["Favorable conditions for planting"]
        })
    
    return planting_days


def generate_harvesting_days(forecast: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate optimal harvesting days based on forecast"""
    harvesting_days = []
    
    for day in forecast:
        # Ideal harvesting conditions: dry weather, mild temperatures
        temp_good = day.get("max_temp", 25) < 30
        rain_good = day.get("pop", 0) < 0.3
        
        if temp_good and rain_good:
            quality = "excellent"
        elif temp_good or rain_good:
            quality = "good"
        else:
            quality = "poor"
        
        reasons = []
        if not temp_good:
            reasons.append("High temperatures may reduce quality")
        
        if not rain_good:
            reasons.append("Rain may make harvesting difficult")
        
        harvesting_days.append({
            "date": day["date"],
            "day_name": day["day_name"],
            "quality": quality,
            "reasons": reasons if reasons else ["Favorable conditions for harvesting"]
        })
    
    return harvesting_days


def generate_pest_warnings(temp: float, humidity: int, weather_condition: str) -> List[Dict[str, Any]]:
    """Generate pest and disease warnings based on weather conditions"""
    warnings = []
    
    # Fungal disease risk (high humidity, moderate temperatures)
    if humidity > 70 and 15 <= temp <= 25:
        warnings.append({
            "type": "fungal",
            "risk": "high",
            "pests": ["Powdery mildew", "Leaf spot", "Blight"],
            "advice": "Increase spacing between plants for better airflow. Avoid overhead watering."
        })
    elif humidity > 60 and 10 <= temp <= 28:
        warnings.append({
            "type": "fungal",
            "risk": "moderate",
            "pests": ["Powdery mildew", "Root rot"],
            "advice": "Monitor plants closely. Water at the base rather than leaves."
        })
    
    # Insect pest risk (warm temperatures)
    if temp > 25:
        warnings.append({
            "type": "insect",
            "risk": "high",
            "pests": ["Aphids", "Spider mites", "Whiteflies"],
            "advice": "Check undersides of leaves regularly. Consider neem oil or insecticidal soap."
        })
    elif temp > 20:
        warnings.append({
            "type": "insect",
            "risk": "moderate",
            "pests": ["Aphids", "Beetles"],
            "advice": "Monitor plants for signs of insect damage."
        })
    
    # Slug risk (rainy, humid conditions)
    if weather_condition in ["rain", "drizzle"] and humidity > 70:
        warnings.append({
            "type": "mollusc",
            "risk": "high",
            "pests": ["Slugs", "Snails"],
            "advice": "Apply slug deterrents. Check plants in the evening with a flashlight."
        })
    
    return warnings


def generate_garden_tasks(current: Dict[str, Any], forecast: List[Dict[str, Any]]) -> List[str]:
    """Generate garden tasks based on weather conditions"""
    tasks = []
    
    # Current weather conditions
    temp = current.get("main", {}).get("temp", 20)
    weather_condition = current.get("weather", [{}])[0].get("main", "").lower()
    
    # Check for upcoming weather events
    rain_coming = False
    frost_coming = False
    heat_coming = False
    
    for day in forecast[:3]:  # Check next 3 days
        if day.get("pop", 0) > 0.5:
            rain_coming = True
        if day.get("min_temp", 10) < 2:
            frost_coming = True
        if day.get("max_temp", 20) > 30:
            heat_coming = True
    
    # Generate tasks based on conditions
    if weather_condition in ["clear", "clouds"] and not rain_coming:
        tasks.append("Good time to apply fertilizer")
    
    if rain_coming:
        tasks.append("Cover sensitive plants before rain arrives")
        tasks.append("Ensure proper drainage to prevent waterlogging")
    
    if frost_coming:
        tasks.append("Protect tender plants from upcoming frost")
        tasks.append("Harvest frost-sensitive vegetables")
    
    if heat_coming:
        tasks.append("Apply mulch to retain soil moisture")
        tasks.append("Set up shade cloth for sensitive plants")
    
    if temp > 25:
        tasks.append("Check irrigation systems and increase watering if needed")
    
    if weather_condition in ["rain", "drizzle"]:
        tasks.append("Good time for transplanting")
        tasks.append("Hold off on pruning until dry weather returns")
    
    # Add some general seasonal tasks
    month = datetime.now().month
    if 3 <= month <= 5:  # Spring
        tasks.append("Start sowing warm-season crops")
        tasks.append("Begin regular pest monitoring")
    elif 6 <= month <= 8:  # Summer
        tasks.append("Monitor for signs of drought stress")
        tasks.append("Harvest mature vegetables promptly")
    elif 9 <= month <= 11:  # Fall
        tasks.append("Begin preparing garden for cooler weather")
        tasks.append("Consider planting cover crops")
    else:  # Winter
        tasks.append("Plan next season's garden layout")
        tasks.append("Maintain composting during winter months")
    
    return tasks


def generate_packing_list(forecast: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Generate packing recommendations based on forecast"""
    clothing = []
    accessories = []
    essentials = []
    
    # Get min/max temperatures across trip
    min_temps = [day.get("min_temp", 20) for day in forecast]
    max_temps = [day.get("max_temp", 20) for day in forecast]
    
    if not min_temps or not max_temps:
        return {
            "clothing": ["Unable to generate recommendations"],
            "accessories": [],
            "essentials": ["Check local weather before packing"]
        }
    
    trip_min_temp = min(min_temps)
    trip_max_temp = max(max_temps)
    
    # Check for weather conditions
    weather_conditions = [day.get("weather", "").lower() for day in forecast]
    has_rain = any(cond in ["rain", "drizzle", "thunderstorm"] for cond in weather_conditions)
    has_snow = any(cond == "snow" for cond in weather_conditions)
    has_wind = any(day.get("wind_speed", 0) > 5 for day in forecast)
    has_sun = any(cond == "clear" for cond in weather_conditions)
    
    # Base temperature-appropriate clothing
    if trip_min_temp < 5:
        clothing.extend([
            "Heavy coat or parka",
            "Thermal underlayers",
            "Sweaters/fleeces",
            "Warm pants",
            "Thick socks"
        ])
        accessories.extend([
            "Winter hat",
            "Gloves/mittens",
            "Scarf"
        ])
    elif trip_min_temp < 15:
        clothing.extend([
            "Light jacket or coat",
            "Long-sleeved shirts",
            "Sweater or hoodie",
            "Pants/jeans"
        ])
        accessories.append("Light gloves if evenings are cool")
    
    if trip_max_temp > 25:
        clothing.extend([
            "T-shirts",
            "Shorts",
            "Light pants",
            "Light dresses/skirts"
        ])
        accessories.extend([
            "Sunglasses",
            "Sun hat"
        ])
        essentials.append("Sunscreen")
    
    # Add for rain/snow
    if has_rain:
        clothing.append("Waterproof jacket/rain coat")
        accessories.extend([
            "Umbrella",
            "Waterproof shoes/boots"
        ])
    
    if has_snow:
        clothing.append("Snow boots")
        accessories.append("Waterproof gloves")
        essentials.append("Lip balm for dry conditions")
    
    # Add for wind
    if has_wind:
        clothing.append("Windbreaker")
        accessories.append("Secure hat that won't blow away")
    
    # Add for sun
    if has_sun:
        if "Sunglasses" not in accessories:
            accessories.append("Sunglasses")
        essentials.extend([
            "Sunscreen",
            "After-sun lotion"
        ])
    
    # Always add essentials
    essentials.extend([
        "Travel-sized toiletries",
        "Any necessary medications",
        "Phone charger",
        "Travel documents"
    ])
    
    # Remove duplicates and sort
    clothing = sorted(list(set(clothing)))
    accessories = sorted(list(set(accessories)))
    essentials = sorted(list(set(essentials)))
    
    return {
        "clothing": clothing,
        "accessories": accessories,
        "essentials": essentials
    }


def generate_activity_recommendations(forecast: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate activity recommendations based on forecast"""
    activities = []
    
    for day in forecast:
        date = day.get("date", "Unknown")
        day_name = day.get("day_name", "Unknown")
        weather = day.get("weather", "").lower()
        max_temp = day.get("max_temp", 20)
        min_temp = day.get("min_temp", 10)
        wind_speed = day.get("wind_speed", 0)
        pop = day.get("pop", 0)
        
        # Generate recommended activities based on conditions
        recommended = []
        not_recommended = []
        
        # Good weather activities
        if weather in ["clear", "clouds"] and pop < 0.3:
            if max_temp > 25:
                recommended.extend([
                    "Beach visits",
                    "Swimming",
                    "Water parks"
                ])
            
            if 15 <= max_temp <= 28:
                recommended.extend([
                    "Hiking",
                    "Outdoor dining",
                    "Sightseeing",
                    "Park visits"
                ])
            
            if max_temp < 28 and wind_speed < 5:
                recommended.append("Cycling")
        
        # Rainy day activities
        if weather in ["rain", "drizzle", "thunderstorm"] or pop > 0.5:
            recommended.extend([
                "Museum visits",
                "Indoor shopping",
                "Local cuisine at restaurants",
                "Spa treatments"
            ])
            
            not_recommended.extend([
                "Beach activities",
                "Hiking",
                "Outdoor sports"
            ])
        
        # Hot day recommendations
        if max_temp > 30:
            recommended.extend([
                "Indoor activities with air conditioning",
                "Water activities",
                "Early morning or evening outings"
            ])
            
            not_recommended.extend([
                "Extensive walking tours",
                "Midday outdoor activities"
            ])
        
        # Cold day recommendations
        if max_temp < 5:
            recommended.extend([
                "Indoor cultural activities",
                "Coffee shops and cafes",
                "Shopping districts"
            ])
            
            if min_temp < 0:
                not_recommended.extend([
                    "Extended outdoor activities without proper gear",
                    "Water sports"
                ])
        
        # Wind considerations
        if wind_speed > 8:
            not_recommended.extend([
                "Boating",
                "Paragliding",
                "Beach umbrellas may be difficult"
            ])
        
        # Remove duplicates
        recommended = list(set(recommended))
        not_recommended = list(set(not_recommended))
        
        activities.append({
            "date": date,
            "day_name": day_name,
            "weather": day.get("weather", "Unknown"),
            "temperature": f"{min_temp}°C to {max_temp}°C",
            "recommended": recommended,
            "not_recommended": not_recommended
        })
    
    return activities


def generate_weather_risks(forecast: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate weather risks to prepare for"""
    risks = []
    
    for day in forecast:
        date = day.get("date", "Unknown")
        day_name = day.get("day_name", "Unknown")
        weather = day.get("weather", "").lower()
        max_temp = day.get("max_temp", 20)
        min_temp = day.get("min_temp", 10)
        wind_speed = day.get("wind_speed", 0)
        pop = day.get("pop", 0)
        
        daily_risks = []
        
        # Check for various risk factors
        if weather == "thunderstorm":
            daily_risks.append({
                "type": "thunderstorm",
                "severity": "high",
                "advice": "Seek indoor shelter. Avoid open areas and water activities."
            })
        
        if pop > 0.7:
            daily_risks.append({
                "type": "heavy_rain",
                "severity": "moderate",
                "advice": "Bring waterproof gear and shoes. Check for flood warnings."
            })
        elif pop > 0.4:
            daily_risks.append({
                "type": "rain",
                "severity": "low",
                "advice": "Pack umbrella or light rain jacket."
            })
        
        if max_temp > 32:
            daily_risks.append({
                "type": "extreme_heat",
                "severity": "high",
                "advice": "Stay hydrated. Avoid midday sun. Seek air-conditioned spaces."
            })
        elif max_temp > 28:
            daily_risks.append({
                "type": "heat",
                "severity": "moderate",
                "advice": "Use sunscreen. Drink plenty of water. Take shade breaks."
            })
        
        if min_temp < 0:
            daily_risks.append({
                "type": "freezing",
                "severity": "moderate",
                "advice": "Pack warm layers. Watch for icy surfaces."
            })
        elif min_temp < 5:
            daily_risks.append({
                "type": "cold",
                "severity": "low",
                "advice": "Bring a jacket for morning and evening."
            })
        
        if wind_speed > 10:
            daily_risks.append({
                "type": "strong_wind",
                "severity": "moderate",
                "advice": "Secure loose items. Be cautious in exposed areas."
            })
        
        if weather == "snow":
            daily_risks.append({
                "type": "snow",
                "severity": "moderate",
                "advice": "Check road conditions. Pack warm, waterproof clothing."
            })
        
        if daily_risks:
            risks.append({
                "date": date,
                "day_name": day_name,
                "risks": daily_risks
            })
    
    return risks


def generate_temperature_change_notification(forecast: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Generate notification for significant temperature changes"""
    if len(forecast) < 2:
        return None
    
    # Check for significant temp changes between days
    for i in range(len(forecast) - 1):
        current_max = forecast[i].get("max_temp")
        next_max = forecast[i+1].get("max_temp")
        
        if current_max is None or next_max is None:
            continue
        
        temp_diff = next_max - current_max
        
        if abs(temp_diff) >= 5:  # 5°C is a significant change
            direction = "rise" if temp_diff > 0 else "drop"
            day_name = forecast[i+1].get("day_name", "tomorrow")
            
            return {
                "type": "temperature_change",
                "priority": "medium",
                "title": f"Temperature {direction} on {day_name}",
                "message": f"Prepare for a {abs(round(temp_diff))}°C temperature {direction} from {round(current_max)}°C to {round(next_max)}°C.",
                "icon": "temperature-change"
            }
    
    return None


def generate_precipitation_notification(forecast: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Generate notification for upcoming precipitation"""
    for i, day in enumerate(forecast):
        pop = day.get("pop", 0)
        weather = day.get("weather", "").lower()
        day_name = day.get("day_name", f"day {i+1}")
        
        # High chance of precipitation
        if pop >= 0.7:
            precip_type = "rain"
            if weather == "snow":
                precip_type = "snow"
            elif weather == "thunderstorm":
                precip_type = "thunderstorms"
            
            return {
                "type": "precipitation",
                "priority": "high",
                "title": f"{precip_type.capitalize()} expected on {day_name}",
                "message": f"High chance ({int(pop*100)}%) of {precip_type} on {day_name}. Plan indoor activities or bring appropriate gear.",
                "icon": precip_type
            }
        # Moderate chance of precipitation (first occurrence)
        elif pop >= 0.4 and i <= 2:  # Only alert for moderate chance in next 3 days
            return {
                "type": "precipitation",
                "priority": "medium",
                "title": f"Possible rain on {day_name}",
                "message": f"Moderate chance ({int(pop*100)}%) of precipitation on {day_name}. Consider bringing rain gear.",
                "icon": "cloudy-rain"
            }
    
    return None


def generate_severe_weather_notification(forecast: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Generate notification for severe weather conditions"""
    for i, day in enumerate(forecast):
        weather = day.get("weather", "").lower()
        day_name = day.get("day_name", f"day {i+1}")
        max_temp = day.get("max_temp")
        min_temp = day.get("min_temp")
        
        # Check for extreme temperatures
        if max_temp is not None and max_temp > 35:
            return {
                "type": "extreme_heat",
                "priority": "high",
                "title": f"Extreme heat on {day_name}",
                "message": f"Temperatures expected to reach {round(max_temp)}°C on {day_name}. Stay hydrated and avoid extended sun exposure.",
                "icon": "extreme-heat"
            }
        
        if min_temp is not None and min_temp < -10:
            return {
                "type": "extreme_cold",
                "priority": "high",
                "title": f"Extreme cold on {day_name}",
                "message": f"Temperatures expected to drop to {round(min_temp)}°C on {day_name}. Limit time outdoors and dress in layers.",
                "icon": "extreme-cold"
            }
        
        # Check for severe weather conditions
        if weather == "thunderstorm":
            return {
                "type": "thunderstorm",
                "priority": "high",
                "title": f"Thunderstorms on {day_name}",
                "message": f"Thunderstorms expected on {day_name}. Stay indoors during storms and be prepared for possible power outages.",
                "icon": "thunderstorm"
            }
    
    return None


def generate_activity_opportunity_notification(forecast: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Generate notification for ideal weather conditions for activities"""
    ideal_days = []
    
    for day in forecast:
        weather = day.get("weather", "").lower()
        max_temp = day.get("max_temp")
        min_temp = day.get("min_temp")
        pop = day.get("pop", 0)
        day_name = day.get("day_name")
        
        # Check for ideal outdoor conditions
        if (weather in ["clear", "clouds"] and
                pop < 0.2 and
                max_temp is not None and
                min_temp is not None and
                18 <= max_temp <= 28 and
                min_temp >= 10):
            ideal_days.append(day_name)
    
    if ideal_days:
        if len(ideal_days) == 1:
            return {
                "type": "ideal_weather",
                "priority": "low",
                "title": f"Perfect weather on {ideal_days[0]}",
                "message": f"Ideal conditions for outdoor activities on {ideal_days[0]}. Great day for hiking, picnics, or any outdoor plans.",
                "icon": "sunny"
            }
        else:
            days_text = ", ".join(ideal_days[:-1]) + " and " + ideal_days[-1] if len(ideal_days) > 1 else ideal_days[0]
            return {
                "type": "ideal_weather",
                "priority": "low",
                "title": "Perfect weather ahead",
                "message": f"Ideal conditions for outdoor activities on {days_text}. Great days for hiking, picnics, or any outdoor plans.",
                "icon": "sunny"
            }
    
    return None


def generate_dry_spell_notification(forecast: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Generate notification for extended periods without rain"""
    if len(forecast) < 3:
        return None
    
    # Check for dry spell (low precipitation chance across multiple days)
    dry_spell = True
    for day in forecast:
        if day.get("pop", 0) > 0.3:  # 30% chance of precipitation or higher
            dry_spell = False
            break
    
    if dry_spell:
        forecast_length = len(forecast)
        return {
            "type": "dry_spell",
            "priority": "medium",
            "title": f"Dry spell for next {forecast_length} days",
            "message": f"No significant rain expected for the next {forecast_length} days. Good opportunity for outdoor projects that require dry weather.",
            "icon": "drought"
        }
    
    return None
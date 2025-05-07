
import os
import csv
from datetime import datetime
import requests
from pathlib import Path

OPENWEATHER_API_KEY = "211fcd6d38d6d8cb1fafd3bfb7721881"  # Your API key from the logs
CITIES = {
    'London': {'lat': 51.5074, 'lon': -0.1278},
    'New York': {'lat': 40.7128, 'lon': -74.0060},
    'Tokyo': {'lat': 35.6762, 'lon': 139.6503},
    'Paris': {'lat': 48.8566, 'lon': 2.3522},
    'Sydney': {'lat': -33.8688, 'lon': 151.2093},
    'Dubai': {'lat': 25.2048, 'lon': 55.2708},
    'Singapore': {'lat': 1.3521, 'lon': 103.8198},
    'Mumbai': {'lat': 19.0760, 'lon': 72.8777}
}

def get_weather_data(lat, lon):
    """Fetch weather data for given coordinates"""
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def scrape_and_save():
    """Scrape weather data for all cities and save to CSV"""
    # Create data directory if it doesn't exist
    data_dir = Path("static/data")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # CSV file path with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = data_dir / f"weather_data_{timestamp}.csv"
    
    # CSV headers
    headers = ['City', 'Temperature', 'Humidity', 'Pressure', 'Wind Speed', 'Weather Description', 'Timestamp']
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for city, coords in CITIES.items():
            data = get_weather_data(coords['lat'], coords['lon'])
            if data:
                row = [
                    city,
                    data['main']['temp'],
                    data['main']['humidity'],
                    data['main']['pressure'],
                    data['wind']['speed'],
                    data['weather'][0]['description'],
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ]
                writer.writerow(row)
                print(f"Added data for {city}")
    
    print(f"Data saved to {csv_file}")
    return str(csv_file)

if __name__ == "__main__":
    scrape_and_save()

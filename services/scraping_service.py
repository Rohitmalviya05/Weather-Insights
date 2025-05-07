
import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class WeatherScraper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.csv_path = "static/data/weather_history.csv"
        
    def scrape_historical_data(self, city: str, days: int = 30) -> List[Dict]:
        """Scrape weather data for the past n days"""
        data = []
        current_date = datetime.now()
        
        try:
            # Get city coordinates first
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={self.api_key}"
            geo_response = requests.get(geo_url)
            geo_data = geo_response.json()
            
            if not geo_data:
                logger.error(f"City not found: {city}")
                return data
                
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']
            
            # Collect data for each day
            for i in range(days):
                date = current_date - timedelta(days=i)
                weather_url = f"{self.base_url}/weather?lat={lat}&lon={lon}&units=metric&appid={self.api_key}"
                
                response = requests.get(weather_url)
                if response.status_code == 200:
                    weather_data = response.json()
                    data.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'city': city,
                        'temperature': weather_data['main']['temp'],
                        'humidity': weather_data['main']['humidity'],
                        'weather_condition': weather_data['weather'][0]['main'],
                        'wind_speed': weather_data['wind']['speed']
                    })
                else:
                    logger.error(f"Error fetching data for {city} on {date}")
                    
            return data
            
        except Exception as e:
            logger.error(f"Error scraping data: {e}")
            return data
            
    def save_to_csv(self, data: List[Dict]) -> bool:
        """Save scraped data to CSV file"""
        try:
            df = pd.DataFrame(data)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
            
            # If file exists, append without headers
            if os.path.exists(self.csv_path):
                df.to_csv(self.csv_path, mode='a', header=False, index=False)
            else:
                df.to_csv(self.csv_path, index=False)
                
            return True
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
            return False
            
    def get_historical_trends(self, city: str) -> Dict:
        """Get trends from stored CSV data"""
        try:
            if not os.path.exists(self.csv_path):
                return {"error": "No historical data available"}
                
            df = pd.read_csv(self.csv_path)
            city_data = df[df['city'] == city]
            
            if city_data.empty:
                return {"error": f"No data available for {city}"}
                
            trends = {
                "avg_temperature": city_data['temperature'].mean(),
                "max_temperature": city_data['temperature'].max(),
                "min_temperature": city_data['temperature'].min(),
                "common_conditions": city_data['weather_condition'].value_counts().to_dict(),
                "avg_humidity": city_data['humidity'].mean(),
                "avg_wind_speed": city_data['wind_speed'].mean()
            }
            
            return trends
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            return {"error": str(e)}

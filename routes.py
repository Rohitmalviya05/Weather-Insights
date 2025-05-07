"""
Routes for the weather application.

This module defines the routes for the Flask application, including:
- Main pages
- API endpoints for weather data
"""

import os
import logging
import json
import random
from datetime import datetime
from datetime import timedelta

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
import requests
from flask import Blueprint, Response
import csv
from io import StringIO

main_bp = Blueprint('main', __name__)

@main_bp.route('/download_csv/<location>')
def download_csv(location):
    # Simulated historical data (you would query your database or API here)
    historical_data = [
        {'date': '2024-05-01', 'temperature': 25, 'humidity': 60},
        {'date': '2024-05-02', 'temperature': 27, 'humidity': 58},
        {'date': '2024-05-03', 'temperature': 26, 'humidity': 63},
    ]

    # Create CSV in memory
    si = StringIO()
    writer = csv.DictWriter(si, fieldnames=["date", "temperature", "humidity"])
    writer.writeheader()
    writer.writerows(historical_data)

    output = si.getvalue()
    si.close()

    # Return as downloadable file
    return Response(
        output,
        mimetype='text/csv',
        headers={
            "Content-Disposition": f"attachment; filename={location}_weather_data.csv"
        }
    )


from services.weather_service import get_weather_for_location, get_forecast_for_location, geocode_location
from services.visualization_service import get_historical_data, export_data_to_csv, create_temperature_chart, analyze_health_trends
# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

@main_bp.before_request
def before_request():
    """Execute before each request to main blueprint"""
    pass

# Main route pages
@main_bp.route('/')
def index():
    """Home page with current weather and basic forecast"""
    from services.analytics_service import get_visitor_stats, track_visit
    track_visit(request, 'home')
    visitor_stats = get_visitor_stats(days=30)
    return render_template('index.html', active_page='home', visitor_stats=visitor_stats)

@main_bp.route('/hyper-local')
def hyper_local():
    """Hyper-localized neighborhood-level weather forecasts"""
    return render_template('hyper_local.html', active_page='hyper-local')

@main_bp.route('/health-alerts')
def health_alerts():
    """Weather-related health alerts and recommendations"""
    return render_template('health_alerts.html', active_page='health-alerts')

@main_bp.route('/clothing-recommendations')
def clothing_recommendations():
    """AI-powered clothing and gear recommendations"""
    return render_template('clothing_recommendations.html', active_page='clothing-recommendations')

@main_bp.route('/historical-trends')
def historical_trends():
    """Weather trends and historical insights"""
    return render_template('historical_trends.html', active_page='historical-trends')

@main_bp.route('/commute-forecast')
def commute_forecast():
    """Travel and commute forecast with route planning"""
    return render_template('commute_forecast.html', active_page='commute-forecast')

@main_bp.route('/gardening-weather')
def gardening_weather():
    """Gardening and agriculture weather tools"""
    return render_template('gardening_weather.html', active_page='gardening-weather')

@main_bp.route('/trip-planner')
def trip_planner():
    """Trip forecasts and packing list generator"""
    return render_template('trip_planner.html', active_page='trip-planner')

@main_bp.route('/smart-notifications')
def smart_notifications():
    """Smart weather notifications and alerts"""
    return render_template('smart_notifications.html', active_page='smart-notifications')

@main_bp.route('/custom-widgets')
def custom_widgets():
    """Custom widgets and API access"""
    return render_template('custom-widgets.html', active_page='custom-widgets')

@main_bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Feedback form"""
    if request.method == 'POST':
        # Process feedback submission
        feedback_type = request.form.get('feedback_type', 'general')
        subject = request.form.get('subject', '')
        message = request.form.get('message', '')
        rating = request.form.get('rating')

        if rating:
            try:
                rating = int(rating)
            except ValueError:
                rating = None

        # TODO: Save feedback to database

        # Redirect to thank you page
        return redirect(url_for('main.thank_you'))

    return render_template('feedback.html', active_page='feedback')

@main_bp.route('/thank-you')
def thank_you():
    """Thank you page after feedback submission"""
    return render_template('thank_you.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        # TODO: Implement login logic
        pass

    return render_template('login.html', active_page='login')

@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup"""
    if request.method == 'POST':
        # TODO: Implement signup logic
        pass

    return render_template('signup.html', active_page='signup')

@main_bp.route('/logout')
def logout():
    """User logout"""
    # TODO: Implement logout logic
    return redirect(url_for('main.index'))

@main_bp.route('/profile')
def profile():
    """User profile and preferences"""
    # TODO: Implement profile page
    return render_template('profile.html', active_page='profile')

@main_bp.route('/weather')
def weather():
    """Weather page"""
    # Get location from query parameters
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    location_name = request.args.get('location')

    # Default to London if no location specified
    if not lat or not lon:
        if location_name:
            # Try to geocode the location name
            geo_data = geocode_location(location_name)
            if geo_data.get('success') and geo_data.get('results'):
                result = geo_data['results'][0]
                lat = result['lat']
                lon = result['lon']
                location_name = result['name']
            else:
                # Default to London if geocoding fails
                lat = 51.5074
                lon = -0.1278
                location_name = 'London'
        else:
            # Default to London
            lat = 51.5074
            lon = -0.1278
            location_name = 'London'

    # Convert coordinates to float
    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        # Handle invalid values
        flash('Invalid coordinates provided.', 'danger')
        return redirect(url_for('main.index'))

    # Get current weather data
    weather_data = get_weather_for_location(lat, lon)
    if not weather_data.get('success'):
        # Handle error
        flash('Unable to fetch weather data. Please try again later.', 'danger')
        return redirect(url_for('main.index'))

    # Get forecast data
    forecast_data = get_forecast_for_location(lat, lon)
    if not forecast_data.get('success'):
        # Handle error
        flash('Unable to fetch forecast data. Please try again later.', 'danger')
        return redirect(url_for('main.index'))

    # Ensure all numeric values are proper types before template rendering
    # Location data
    location = weather_data['location']
    location['lat'] = float(location['lat'])
    location['lon'] = float(location['lon'])
    location['timezone'] = int(location['timezone'])

    # Current weather data
    current = weather_data['current']
    current['temp'] = float(current['temp'])
    current['feels_like'] = float(current['feels_like'])
    current['humidity'] = int(current['humidity'])
    current['pressure'] = int(current['pressure'])
    current['wind_speed'] = float(current['wind_speed'])
    current['visibility'] = int(current['visibility'])
    if 'rain' in current and '1h' in current['rain']:
        current['rain']['1h'] = float(current['rain']['1h'])

    # Forecast data - ensure all numeric values are proper types
    for day in forecast_data['forecast']:
        day['temp_max'] = float(day['temp_max'])
        day['temp_min'] = float(day['temp_min'])
        day['temp_avg'] = float(day['temp_avg'])
        day['humidity_avg'] = int(day['humidity_avg'])
        day['wind_speed_avg'] = float(day['wind_speed_avg'])
        if 'rain_chance' in day:
            day['rain_chance'] = float(day['rain_chance'])

    # Combine data
    combined_data = {
        'success': True,
        'location': location,
        'current': current,
        'forecast': forecast_data['forecast']
    }

    # Get current datetime for the location's timezone
    timestamp = datetime.now().timestamp()
    timezone_offset = location['timezone']
    current_datetime = datetime.fromtimestamp(timestamp + timezone_offset).strftime('%Y-%m-%d %H:%M:%S')

    return render_template('weather.html', 
                           active_page='weather', 
                           weather=combined_data,
                           current_datetime=current_datetime)

@main_bp.route('/map')
def map():
    """Weather map"""
    return render_template('map.html', active_page='map')

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html', active_page='about')

@main_bp.route('/memes')
def memes():
    from services.reddit_scraper import reddit_api
    weather_memes = reddit_api.get_weather_memes(limit=9)
    return render_template('memes.html', memes=weather_memes)

# API routes
@api_bp.route('/check-twilio-credentials')
def check_twilio_credentials():
    """Check if Twilio credentials are available for SMS notifications"""
    twilio_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    twilio_token = os.environ.get("TWILIO_AUTH_TOKEN")
    twilio_phone = os.environ.get("TWILIO_PHONE_NUMBER")

    credentials_available = all([twilio_sid, twilio_token, twilio_phone])

    return jsonify({
        'success': True,
        'credentials_available': credentials_available
    })

@api_bp.route('/check-openai-credentials')
def check_openai_credentials():
    """Check if OpenAI credentials are available for AI-powered features"""
    openai_key = os.environ.get("OPENAI_API_KEY")

    credentials_available = bool(openai_key)

    return jsonify({
        'success': True,
        'credentials_available': credentials_available
    })

@api_bp.route('/weather')
def get_weather():
    """Get current weather data"""
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    units = request.args.get('units', 'metric')

    if not lat or not lon:
        return jsonify({'success': False, 'message': 'Missing latitude or longitude'})

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid latitude or longitude'})

    # Get weather data
    weather_data = get_weather_for_location(lat, lon, units)

    return jsonify(weather_data)

@api_bp.route('/forecast')
def get_forecast():
    """Get weather forecast data"""
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    units = request.args.get('units', 'metric')
    days = request.args.get('days', 7)

    if not lat or not lon:
        return jsonify({'success': False, 'message': 'Missing latitude or longitude'})

    try:
        lat = float(lat)
        lon = float(lon)
        days = int(days)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid parameters'})

    # Get forecast data
    forecast_data = get_forecast_for_location(lat, lon, units, days)

    return jsonify(forecast_data)

@api_bp.route('/historical')
def get_historical():
    """Get historical weather data"""
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    days = request.args.get('days', 30)

    if not lat or not lon:
        return jsonify({'success': False, 'message': 'Missing latitude or longitude'})

    try:
        lat = float(lat)
        lon = float(lon)
        days = int(days)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid parameters'})

    # Get historical data
    historical_data = get_historical_data(lat, lon, days)

    return jsonify(historical_data)

@api_bp.route('/geocode')
def geocode():
    """Geocode a location name to coordinates"""
    location = request.args.get('q')  # Changed from 'location' to 'q' to match the frontend

    if not location:
        return jsonify({'error': 'Missing location name'})

    # Use the OpenWeather API if API key is available
    api_key = current_app.config.get("OPENWEATHER_API_KEY")
    if api_key:
        try:
            url = f"https://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    location_data = data[0]
                    return jsonify({
                        'lat': location_data.get('lat'),
                        'lon': location_data.get('lon'),
                        'name': location_data.get('name', location),
                        'country': location_data.get('country', ''),
                        'state': location_data.get('state', '')
                    })
        except Exception as e:
            print(f"Error geocoding: {e}")

    # Default coordinates for different major cities if API call fails or no match
    city_coordinates = {
        'london': {'lat': 51.5074, 'lon': -0.1278, 'name': 'London', 'country': 'United Kingdom'},
        'new york': {'lat': 40.7128, 'lon': -74.0060, 'name': 'New York', 'country': 'United States'},
        'paris': {'lat': 48.8566, 'lon': 2.3522, 'name': 'Paris', 'country': 'France'},
        'tokyo': {'lat': 35.6762, 'lon': 139.6503, 'name': 'Tokyo', 'country': 'Japan'},
        'sydney': {'lat': -33.8688, 'lon': 151.2093, 'name': 'Sydney', 'country': 'Australia'},
        'beijing': {'lat': 39.9042, 'lon': 116.4074, 'name': 'Beijing', 'country': 'China'},
        'berlin': {'lat': 52.5200, 'lon': 13.4050, 'name': 'Berlin', 'country': 'Germany'},
        'moscow': {'lat': 55.7558, 'lon': 37.6173, 'name': 'Moscow', 'country': 'Russia'},
        'dubai': {'lat': 25.2048, 'lon': 55.2708, 'name': 'Dubai', 'country': 'United Arab Emirates'},
        'rio': {'lat': -22.9068, 'lon': -43.1729, 'name': 'Rio de Janeiro', 'country': 'Brazil'},
        'cape town': {'lat': -33.9249, 'lon': 18.4241, 'name': 'Cape Town', 'country': 'South Africa'},
        'mumbai': {'lat': 19.0760, 'lon': 72.8777, 'name': 'Mumbai', 'country': 'India'},
        'istanbul': {'lat': 41.0082, 'lon': 28.9784, 'name': 'Istanbul', 'country': 'Turkey'},
        'rome': {'lat': 41.9028, 'lon': 12.4964, 'name': 'Rome', 'country': 'Italy'},
        'los angeles': {'lat': 34.0522, 'lon': -118.2437, 'name': 'Los Angeles', 'country': 'United States'},
        'chicago': {'lat': 41.8781, 'lon': -87.6298, 'name': 'Chicago', 'country': 'United States'},
        'toronto': {'lat': 43.6532, 'lon': -79.3832, 'name': 'Toronto', 'country': 'Canada'},
        'cairo': {'lat': 30.0444, 'lon': 31.2357, 'name': 'Cairo', 'country': 'Egypt'}
    }

    # Try to match the location to one of our predefined cities
    location_lower = location.lower()
    for city, coord in city_coordinates.items():
        if city in location_lower or location_lower in city:
            return jsonify(coord)

    # If no match is found among our predefined cities, use New York as default
    return jsonify({
        'lat': 40.7128, 
        'lon': -74.0060, 
        'name': location.title(),  # Use the user input, capitalized
        'country': 'United States' 
    })

@api_bp.route('/reverse-geocode')
def reverse_geocode():
    """Reverse geocode coordinates to location name"""
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({
            'name': 'New York',
            'country': 'United States',
            'state': 'New York',
            'lat': 40.7128,
            'lon': -74.0060
        })

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({
            'name': 'New York',
            'country': 'United States',
            'state': 'New York',
            'lat': 40.7128,
            'lon': -74.0060
        })

    # Use the OpenWeather API if API key is available
    api_key = current_app.config.get("OPENWEATHER_API_KEY")
    if api_key:
        try:
            url = f"https://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    location = data[0]
                    return jsonify({
                        'name': location.get('name', 'Unknown'),
                        'country': location.get('country', ''),
                        'state': location.get('state', ''),
                        'lat': lat,
                        'lon': lon
                    })
        except Exception as e:
            print(f"Error reverse geocoding: {e}")

    # Default response if API call fails or API key is missing
    # Use approximate location based on coordinates
    location_map = {
        # North America
        (25, 50, -130, -60): {'name': 'New York', 'country': 'United States', 'state': 'New York'},
        # Europe
        (35, 60, -10, 40): {'name': 'London', 'country': 'United Kingdom', 'state': 'England'},
        # Asia
        (10, 50, 60, 145): {'name': 'Tokyo', 'country': 'Japan', 'state': ''},
        # South America
        (-60, 15, -80, -30): {'name': 'São Paulo', 'country': 'Brazil', 'state': ''},
        # Africa
        (-40, 35, -20, 55): {'name': 'Cairo', 'country': 'Egypt', 'state': ''},
        # Australia
        (-50, -10, 110, 180): {'name': 'Sydney', 'country': 'Australia', 'state': 'NSW'},
    }

    # Find which region the coordinates are in
    for (min_lat, max_lat, min_lon, max_lon), location in location_map.items():
        if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
            location['lat'] = lat
            location['lon'] = lon
            return jsonify(location)

    # Default response if no region matches
    return jsonify({
        'name': 'New York',
        'country': 'United States',
        'state': 'New York',
        'lat': lat,
        'lon': lon
    })

@api_bp.route('/temperature-chart')
def scrape_weather_data():
    """Endpoint to scrape and return weather data"""
    from services.weather_scraper import scrape_and_save
    try:
        csv_file = scrape_and_save()
        return jsonify({
            'success': True,
            'file': csv_file,
            'message': 'Weather data scraped successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def get_temperature_chart():
    """Get temperature chart for a location"""
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    location = request.args.get('location', 'Unknown Location')

    if not lat or not lon:
        return jsonify({'success': False, 'message': 'Missing latitude or longitude'})

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid latitude or longitude'})

    # Get historical data
    historical_data = get_historical_data(lat, lon)

    # Create chart
    chart_path = create_temperature_chart(location, historical_data)

    if not chart_path:
        return jsonify({'success': False, 'message': 'Failed to create chart'})

    return jsonify({'success': True, 'chart_url': url_for('static', filename=chart_path)})

@api_bp.route('/export-csv')
def export_csv():
    """Export historical data to CSV"""
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    location = request.args.get('location', 'Unknown Location')
    type = request.args.get('type', 'historical')

    if not lat or not lon:
        return jsonify({'success': False, 'message': 'Missing latitude or longitude'})

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid latitude or longitude'})

    # Get data based on type
    if type == 'historical':
        data = get_historical_data(lat, lon)
    else:
        # TODO: Implement other data types
        return jsonify({'success': False, 'message': 'Unsupported data type'})

    # Export to CSV
    csv_path = export_data_to_csv(data, location, type)

    if not csv_path:
        return jsonify({'success': False, 'message': 'Failed to export data'})

    return jsonify({'success': True, 'csv_url': url_for('static', filename=csv_path)})

@api_bp.route('/clothing')
def get_clothing_recommendations():
    """Get clothing recommendations based on weather"""
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    location = request.args.get('location', 'New York')
    gender = request.args.get('gender', 'neutral')
    activity = request.args.get('activity', 'casual')

    # Always return mock data for demonstration
    # This ensures the feature works without requiring API keys
    location_display = location
    if location_display == '':
        location_display = 'New York'

    # Return mock data based on the provided parameters
    clothing_items = {
        'neutral': {
            'casual': {
                'today': [
                    'Light jacket or sweater',
                    'Long-sleeve shirt',
                    'Jeans or light pants',
                    'Comfortable walking shoes'
                ],
                'tonight': [
                    'Medium jacket',
                    'Scarf',
                    'Jeans or pants',
                    'Closed shoes'
                ]
            },
            'work': {
                'today': [
                    'Light blazer or cardigan',
                    'Button-down shirt or blouse',
                    'Chinos or slacks',
                    'Comfortable dress shoes'
                ],
                'tonight': [
                    'Medium-weight blazer',
                    'Light scarf',
                    'Business casual pants',
                    'Closed formal shoes'
                ]
            },
            'formal': {
                'today': [
                    'Suit jacket or blazer',
                    'Formal shirt or blouse',
                    'Dress pants or skirt',
                    'Formal shoes'
                ],
                'tonight': [
                    'Formal overcoat',
                    'Scarf',
                    'Formal attire',
                    'Dress shoes'
                ]
            }
        }
    }

    # Default to casual if activity isn't in our mock data
    if activity not in clothing_items.get(gender, {}) and activity not in clothing_items.get('neutral', {}):
        activity = 'casual'

    # Default to neutral if gender isn't in our mock data
    if gender not in clothing_items:
        gender = 'neutral'

    # Get recommendations for the selected gender and activity
    recommendations = clothing_items.get(gender, {}).get(activity, clothing_items['neutral']['casual'])

    return jsonify({
        'success': True,
        'location': location_display,
        'current': {
            'temp': 18,
            'feels_like': 16,
            'humidity': 65,
            'wind_speed': 8,
            'description': 'Partly cloudy',
            'icon_class': 'fa-cloud-sun'
        },
        'recommendations': recommendations,
        'tips': [
            'The temperature will drop about 5°C in the evening, so bring an extra layer.',
            'No rain is expected, but humidity is high.',
            'UV index is low, no sun protection needed.',
            'Wind will make it feel cooler than the actual temperature.'
        ]
    })

@api_bp.route('/trip-planner')
def get_trip_recommendations():
    """Get trip recommendations and packing list"""
    from datetime import datetime, timedelta
    import random

    destination = request.args.get('destination', 'New York')
    country = request.args.get('country', 'USA')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    # Default dates if none provided
    if not start_date:
        start_date = datetime.now().strftime('%Y-%m-%d')
    if not end_date:
        end_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')

    # Use reliable mock data for demonstration purposes
    # Calculate the number of days between start and end dates
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        num_days = (end - start).days + 1
        if num_days < 1:
            num_days = 5  # Ensure at least 1 day
    except:
        # If date parsing fails, use default dates
        start = datetime.now()
        end = start + timedelta(days=5)
        num_days = 5

    # Create mock forecast data based on the number of days
    days = []
    for i in range(num_days):
        current_date = start + timedelta(days=i)
        formatted_date = current_date.strftime('%a, %b %d')  # e.g., "Mon, Jun 12"

        # Alternate between different weather conditions
        if i % 3 == 0:
            icon = "fa-sun"
            description = "Sunny"
            precipitation = 0
        elif i % 3 == 1:
            icon = "fa-cloud-sun"
            description = "Partly cloudy"
            precipitation = 10
        else:
            icon = "fa-cloud-rain"
            description = "Light rain"
            precipitation = 40

        # Random temperatures between 20-28°C for day, 15-20°C for night
        day_temp = round(random.uniform(20, 28), 1)
        night_temp = round(random.uniform(15, 20), 1)

        days.append({
            'date': formatted_date,
            'icon': icon,
            'description': description,
            'precipitation': precipitation,
            'wind': round(random.uniform(5, 15)),
            'temp': {
                'day': day_temp,
                'night': night_temp
            }
        })

    # Choose an overall icon based on the most common condition
    icons = [day['icon'] for day in days]
    overall_icon = max(set(icons), key=icons.count)

    # Format dates for display
    formatted_start = start.strftime('%b %d, %Y')
    formatted_end = end.strftime('%b %d, %Y')

    # Create activity recommendations based on the weather patterns
    activities = []
    rainy_days = [i for i, day in enumerate(days) if 'rain' in day['icon']]
    sunny_days = [i for i, day in enumerate(days) if 'sun' in day['icon'] and 'cloud' not in day['icon']]

    if sunny_days:
        activities.append(f"Days {', '.join([str(d+1) for d in sunny_days])} will be perfect for outdoor activities")

    if rainy_days:
        activities.append(f"Consider indoor activities on days {', '.join([str(d+1) for d in rainy_days])}")

    activities.append("Mornings will generally be cooler - ideal for sightseeing")
    activities.append("Evenings are pleasant for outdoor dining most days")

    return jsonify({
        'success': True,
        'destination': destination,
        'country': country,
        'start_date': formatted_start,
        'end_date': formatted_end,
        'days': days,
        'overall_icon': overall_icon,
        'packing_list': {
            'essentials': [
                'Passport and travel documents',
                'Local currency',
                'Phone charger and adapter',
                'Medications'
            ],
            'clothing': [
                'Light t-shirts',
                'Shorts or light pants',
                'One light jacket for evenings',
                'Comfortable walking shoes',
                'Swimwear'
            ],
            'weather_specific': [
                'Sunscreen (SPF 30+)',
                'Sunglasses',
                'Hat or cap',
                'Small umbrella'
            ]
        },
        'activities': activities,
        'weather_notes': [
            f"Weather in {destination} varies throughout your stay, with an overall trend of warm days and cooler nights.",
            "Pack layers that can be added or removed throughout the day.",
            "Be prepared for occasional rain showers by having a small umbrella."
        ]
    })

@api_bp.route('/health-alerts')
def get_health_alerts():
    """Get health alerts and recommendations based on weather conditions"""
    from datetime import datetime
    import random
    import os

    lat = request.args.get('lat')
    lon = request.args.get('lon')
    location = request.args.get('location', '')
    age_group = request.args.get('age_group', 'adult')
    conditions = request.args.get('conditions', '')

    if conditions:
        conditions = conditions.split(',')
    else:
        conditions = []

    # Check if we have required parameters
    if not lat or not lon:
        return jsonify({'error': 'Missing latitude or longitude'})

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({'error': 'Invalid latitude or longitude'})

    # Get real weather data if API key is available
    api_key = current_app.config.get("OPENWEATHER_API_KEY")
    current_weather = None

    if api_key:
        try:
            # Get current weather data
            weather_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&units=metric&appid={api_key}"
            response = requests.get(weatherurl)

            if response.status_code == 200:
                data = response.json()

                if data:
                    # Extractcurrent weather
                    current_weather = {
                        'dt': data['current']['dt'],
                        'temp': data['current']['temp'],
                        'feels_like': data['current']['feels_like'],
                        'humidity': data['current']['humidity'],
                        'pressure': data['current']['pressure'],
                        'wind_speed': data['current']['wind_speed'],
                        'uvi': data['current'].get('uvi', 4.0),
                        'weather': data['current']['weather']
                    }

                    # Update daily forecast with real data
                    daily_forecast = []
                    today = datetime.now()

                    for i, day in enumerate(data['daily'][:5]):  # Use first 5 days
                        daily_forecast.append({
                            'dt': day['dt'],
                            'temp': day['temp'],
                            'weather': day['weather'],
                            'humidity': day['humidity'],
                            'pressure': day['pressure'],
                            'wind_speed': day['wind_speed'],
                            'uvi': day.get('uvi', 4.0),
                            'air_quality_index': random.randint(40, 70),  # Random AQI since not in OpenWeather free
                            'pollen_level': random.randint(2, 5),  # Random pollen since not in OpenWeather free
                            'health_risk': random.randint(2, 8)  # Calculate risk based on conditions
                        })

                    # Use the real forecast data for alerts
                    return generate_health_alerts_response(current_weather, daily_forecast, age_group, conditions)
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            # Fall back to sample data if API call fails

    # If we couldn't get real data, use sample data with some location-based variations
    # Make temperature vary by latitude to simulate different climates
    base_temp = 25

    # Adjust temperature based on latitude (cooler toward poles, warmer near equator)
    if abs(lat) > 60:  # Polar regions
        base_temp = 5
    elif abs(lat) > 40:  # Temperate regions
        base_temp = 15
    elif abs(lat) > 20:  # Subtropical regions
        base_temp = 25
    else:  # Tropical regions
        base_temp = 30

    # Add seasonal variations in the temperature
    month = datetime.now().month
    if (month >= 12 or month <= 2):  # Winter in Northern Hemisphere
        if lat > 0:  # Northern Hemisphere
            base_temp -= 10
        else:  # Southern Hemisphere (summer)
            base_temp += 5
    elif (month >= 6 and month <= 8):  # Summer in Northern Hemisphere
        if lat > 0:  # Northern Hemisphere
            base_temp += 5
        else:  # Southern Hemisphere (winter)
            base_temp -= 10

    # Add some random variation
    temp_variation = random.uniform(-5, 5)

    # Get weather condition based on location
    weather_conditions = ['Clear', 'Clouds', 'Rain', 'Snow', 'Thunderstorm', 'Mist']
    weather_descriptions = ['clear sky', 'partly cloudy', 'light rain', 'light snow', 'thunderstorm', 'mist']

    # Pick weather condition based on location and temperature
    weather_index = 0
    if base_temp < 0:
        weather_index = 3  # Snow
    elif base_temp < 10:
        weather_index = random.choice([1, 4, 5])  # Clouds, Mist, or Thunderstorm
    elif base_temp < 20:
        weather_index = random.choice([0, 1, 2])  # Clear, Clouds, or Rain
    else:
        weather_index = random.choice([0, 1, 2, 4])  # Clear, Clouds, Rain, or Thunderstorm

    # Create current weather data
    current_weather = {
        'dt': int(datetime.now().timestamp()),
        'temp': base_temp + temp_variation,
        'feels_like': base_temp + temp_variation - 2,
        'humidity': random.randint(40, 80),
        'pressure': random.randint(990, 1030),
        'wind_speed': random.uniform(1.0, 10.0),
        'uvi': random.uniform(1.0, 8.0),
        'weather': [
            {
                'id': 800 + weather_index,
                'main': weather_conditions[weather_index],
                'description': weather_descriptions[weather_index],
                'icon': f'0{weather_index + 1}d'
            }
        ]
    }

    # Create daily forecast with location-specific variations
    daily_forecast = []
    today = datetime.now()

    # Generate forecasts that make some meteorological sense
    prev_temp = current_weather['temp']

    for i in range(5):  # 5-day forecast
        # Temperature tends to be more stable with smaller variations between consecutive days
        daily_temp = prev_temp + random.uniform(-3, 3)

        # Keep temperature in a reasonable range
        if daily_temp > 35:
            daily_temp = 35 - random.uniform(0, 5)
        elif daily_temp < -15:
            daily_temp = -15 + random.uniform(0, 5)

        prev_temp = daily_temp

        # Weather conditions transition realistically
        # More likely to be similar to previous day with occasional changes
        if i == 0:
            weather_main = current_weather['weather'][0]['main']
            weather_icon = f'0{weather_index + 1}d'
        else:
            # 70% chance to keep similar weather, 30% chance to change
            if random.random() < 0.7:
                weather_main = daily_forecast[i-1]['weather']['main']
                weather_icon = daily_forecast[i-1]['weather']['icon']
            else:
                # Pick a new weather condition
                weather_conditions = ['Clear', 'Clouds', 'Rain', 'Snow', 'Thunderstorm', 'Mist']
                weather_icons = ['01d', '03d', '10d', '13d', '11d', '50d']

                # Select weather based on temperature
                if daily_temp < 0:
                    # Higher chance of snow when cold
                    idx = random.choices(range(6), weights=[0.05, 0.2, 0.1, 0.5, 0.05, 0.1])[0]
                elif daily_temp < 10:
                    # Mix of conditions in cool weather
                    idx = random.choices(range(6), weights=[0.2, 0.3, 0.2, 0.1, 0.1, 0.1])[0]
                else:
                    # Higher chance of clear/clouds in warm weather
                    idx = random.choices(range(6), weights=[0.3, 0.3, 0.2, 0.0, 0.1, 0.1])[0]

                weather_main = weather_conditions[idx]
                weather_icon = weather_icons[idx]

        # Air quality is often correlated with weather conditions
        # Clear days tend to have better air quality, rainy days can clean air
        if weather_main == 'Clear':
            air_quality = random.randint(30, 50)  # Good to Moderate
        elif weather_main == 'Rain':
            air_quality = random.randint(20, 40)  # Good (rain cleans air)
        elif weather_main == 'Thunderstorm':
            air_quality = random.randint(30, 60)  # Variable
        elif weather_main == 'Snow':
            air_quality = random.randint(40, 60)  # Moderate
        else:
            air_quality = random.randint(40, 70)  # Moderate to Unhealthy for Sensitive Groups

        # Pollen levels are seasonal and affected by weather
        # Rain reduces pollen, dry and windy increases it
        if weather_main in ['Rain', 'Snow', 'Thunderstorm']:
            pollen = random.randint(1, 3)  # Low when wet
        elif weather_main == 'Clear' and current_weather['wind_speed'] > 5:
            pollen = random.randint(4, 7)  # High on clear, windy days
        else:
            pollen = random.randint(2, 5)  # Moderate otherwise

        # UV index is higher on clear days and at lower latitudes
        if weather_main == 'Clear':
            uv_base = 7
        elif weather_main == 'Clouds':
            uv_base = 5
        else:
            uv_base = 3

        # Adjust UV for latitude (higher near equator)
        if abs(lat) < 20:
            uv_base += 2
        elif abs(lat) > 50:
            uv_base -= 2

        uv_index = max(1, min(11, int(uv_base + random.uniform(-1, 1))))

        # Health risk calculation - more severe with extreme weather, high UV, poor air quality
        health_factors = 0
        if daily_temp > 30 or daily_temp < 0:
            health_factors += 2  # Extreme temperatures
        if uv_index > 7:
            health_factors += 2  # High UV
        if air_quality > 50:
            health_factors += 2  # Poor air quality
        if pollen > 5:
            health_factors += 2  # High pollen

        # Adjust for forecast day (less certainty farther out)
        health_risk = min(10, health_factors + random.randint(1, 3))

        daily_forecast.append({
            'day': (today + timedelta(days=i)).strftime('%A'),
            'date': (today + timedelta(days=i)).strftime('%m/%d'),
            'weather': {
                'main': weather_main,
                'icon': weather_icon
            },
            'temp': daily_temp,
            'air_quality_index': air_quality,
            'pollen_level': pollen,
            'uv_index': uv_index,
            'health_risk': health_risk
        })

    # Generate health alerts based on weather, age group, and conditions
    return generate_health_alerts_response(current_weather, daily_forecast, age_group, conditions)

def generate_health_alerts_response(current_weather, daily_forecast, age_group, conditions):
    alerts = []
    # Generate alerts based on current weather
    if current_weather:
        temp = current_weather['temp']
        if temp > 35:
            alerts.append("Heat alert: Drink plenty of fluids and avoid strenuous activity.")
        elif temp < 0:
            alerts.append("Cold alert: Dress warmly in layers and protect exposed skin.")
        if current_weather['uvi'] > 7:
            alerts.append("High UV alert: Use sunscreen and protective clothing.")
        if 'Rain' in current_weather['weather'][0]['main']:
            alerts.append("Rain alert: Be cautious when driving and watch out for flooding.")
        if 'Thunderstorm' in current_weather['weather'][0]['main']:
            alerts.append("Thunderstorm alert: Seek shelter during storms and avoid contact with water.")

    # Add alerts based on daily forecast
    for day_forecast in daily_forecast:
        # Handle both dictionary and float temperature formats
        if isinstance(day_forecast['temp'], dict):
            temp = day_forecast['temp']['day']
        else:
            temp = day_forecast['temp']  # If temp is directly a float

        if temp > 35:
            alerts.append(f"Heat alert for {day_forecast.get('day', 'upcoming days')}: Drink plenty of fluids and avoid strenuous activity.")
        elif temp < 0:
            alerts.append(f"Cold alert for {day_forecast.get('day', 'upcoming days')}: Dress warmly in layers and protect exposed skin.")
        if day_forecast['uv_index'] > 7:
            alerts.append(f"High UV alert for {day_forecast.get('day', 'upcoming days')}: Use sunscreen and protective clothing.")
        if 'Rain' in day_forecast['weather']['main']:
            alerts.append(f"Rain alert for {day_forecast.get('day', 'upcoming days')}: Be cautious when driving and watch out for flooding.")
        if 'Thunderstorm' in day_forecast['weather']['main']:
            alerts.append(f"Thunderstorm alert for {day_forecast.get('day', 'upcoming days')}: Seek shelter during storms and avoid contact with water.")
        if day_forecast['air_quality_index'] > 50:
            alerts.append(f"Air quality alert for {day_forecast.get('day', 'upcoming days')}: Check air quality levels and avoid strenuous activity if you are sensitive.")
        if day_forecast['pollen_level'] > 5:
            alerts.append(f"Pollen alert for {day_forecast.get('day', 'upcoming days')}: Check pollen levels and take precautions if you have allergies.")
        if day_forecast['health_risk'] > 7:
            alerts.append(f"High health risk for {day_forecast.get('day', 'upcoming days')}: Take extra care and consider avoiding outdoor activities.")



    # Add alerts based on specific conditions
    for condition in conditions:
        if condition == "heat":
            alerts.append("General heat alert: Drink plenty of fluids and take it easy in the heat.")
        elif condition == "cold":
            alerts.append("General cold alert: Dress warmly and protect yourself from the cold.")
        elif condition == "rain":
            alerts.append("General rain alert: Watch out for flooding and be cautious when driving.")
        elif condition == "thunderstorm":
            alerts.append("General thunderstorm alert: Stay indoors during storms.")
        elif condition == "air_quality":
            alerts.append("General air quality alert: Check air quality and take precautions if sensitive.")
        elif condition == "pollen":
            alerts.append("General pollen alert: Check pollen levels and take precautions if you have allergies.")


    # Customize alerts based on age group
    if age_group == "child":
        alerts.extend([
            "Keep children hydrated and indoors during extreme weather conditions.",
            "Monitor children for signs of heat stroke or hypothermia."
        ])
    elif age_group == "elderly":
        alerts.extend([
            "Encourage elderly people to stay hydrated and seek medical attention if experiencing heat stroke or hypothermia.",
            "Check on elderly neighbors during extreme weather."
        ])

    return jsonify({
        'success': True,
        'alerts': alerts,
        'current_weather': current_weather,
        'daily_forecast': daily_forecast
    })

@api_bp.route('/health-trends')
def get_health_trends():
    """Get health trends from scraped weather data"""
    try:
        from services.visualization_service import analyze_health_trends

        csv_file = os.path.join('static', 'data', 'weather_data.csv')
        if not os.path.exists(csv_file):
            return jsonify({
                'success': False,
                'error': 'No weather data available'
            })

        trends = analyze_health_trends(csv_file)
        if not trends:
            return jsonify({
                'success': False,
                'error': 'Error analyzing trends'
            })

        return jsonify({
            'success': True,
            'data': trends
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })
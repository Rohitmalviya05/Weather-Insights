/**
 * Main JavaScript for Weather Insights application
 */

// State for weather app
const weatherState = {
    units: 'metric',
    currentLocation: null,
    weatherData: null,
    forecastData: null
};

// Document ready function
document.addEventListener('DOMContentLoaded', function() {
    console.log('Weather Insights initialized');
    
    // Initialize map if element exists
    const mapElement = document.getElementById('interactive-map');
    if (mapElement) {
        initInteractiveMap(mapElement);
    }
    
    // Initialize current weather if element exists
    const currentWeatherElement = document.getElementById('current-weather');
    if (currentWeatherElement) {
        initCurrentWeather();
    }
    
    // Initialize forecast if element exists
    const forecastElement = document.getElementById('forecast-container');
    if (forecastElement) {
        initForecast();
    }
    
    // Initialize unit toggle if element exists
    const unitToggleElement = document.getElementById('unit-toggle');
    if (unitToggleElement) {
        unitToggleElement.addEventListener('change', function() {
            toggleUnit(this.checked);
        });
    }
});

/**
 * Initialize the interactive weather map 
 */
function initInteractiveMap(mapElement) {
    // Create the Leaflet map
    const map = L.map(mapElement).setView([25, 10], 2);
    
    // Add the base map layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18
    }).addTo(map);
    
    // Add popular cities as markers
    const popularCities = [
        { name: "London", lat: 51.5074, lon: -0.1278, country: "GB" },
        { name: "New York", lat: 40.7128, lon: -74.0060, country: "US" },
        { name: "Tokyo", lat: 35.6762, lon: 139.6503, country: "JP" },
        { name: "Sydney", lat: -33.8688, lon: 151.2093, country: "AU" },
        { name: "Rio de Janeiro", lat: -22.9068, lon: -43.1729, country: "BR" },
        { name: "Cairo", lat: 30.0444, lon: 31.2357, country: "EG" },
        { name: "Moscow", lat: 55.7558, lon: 37.6173, country: "RU" },
        { name: "Paris", lat: 48.8566, lon: 2.3522, country: "FR" },
        { name: "Mumbai", lat: 19.0760, lon: 72.8777, country: "IN" },
        { name: "Singapore", lat: 1.3521, lon: 103.8198, country: "SG" }
    ];
    
    // Create custom marker icon
    const cityIcon = L.icon({
        iconUrl: 'https://cdn-icons-png.flaticon.com/512/3069/3069613.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32],
        shadowSize: [32, 32]
    });
    
    // Add markers for popular cities
    popularCities.forEach(city => {
        const marker = L.marker([city.lat, city.lon], { icon: cityIcon }).addTo(map);
        
        // Fetch weather data when marker is clicked
        marker.on('click', function() {
            fetchCityWeather(city.lat, city.lon, city.name, marker);
        });
    });
    
    // Store map in a global variable so it can be accessed from other functions
    window.map = map;
    
    // Handle map clicks
    map.on('click', function(e) {
        fetchLocationWeather(e.latlng.lat, e.latlng.lng, null, e.latlng);
    });
}

/**
 * Fetch weather data for a clicked location
 */
function fetchLocationWeather(lat, lon, cityName, latlng) {
    // Show loading popup
    const loadingPopup = L.popup()
        .setLatLng(latlng)
        .setContent('<div class="text-center"><div class="spinner-border spinner-border-sm text-primary" role="status"></div><span class="ms-2">Loading weather data...</span></div>')
        .openOn(map);
    
    // Make API call to get weather
    fetch(`/api/weather?lat=${lat}&lon=${lon}`)
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                throw new Error(data.message || 'Failed to fetch weather data');
            }
            
            // Use API data to create weather popup
            const locationName = cityName || data.location.name || 'Unknown Location';
            
            // Create popup content with weather data
            const tempUnit = weatherState.units === 'imperial' ? '°F' : '°C';
            const tempValue = weatherState.units === 'imperial' ? 
                Math.round(data.current.temp * 9/5 + 32) : 
                Math.round(data.current.temp);
            const feelsLikeValue = weatherState.units === 'imperial' ? 
                Math.round(data.current.feels_like * 9/5 + 32) : 
                Math.round(data.current.feels_like);
            const windUnit = weatherState.units === 'imperial' ? 'mph' : 'm/s';
            
            const popupContent = `
                <div class="weather-popup">
                    <h4>${locationName}, ${data.location.country}</h4>
                    <div class="temp">${tempValue}${tempUnit}</div>
                    <div class="description">${data.current.weather.description}</div>
                    <div class="details">
                        <div class="detail">
                            <i class="fas fa-thermometer-half"></i>
                            <span>Feels like: ${feelsLikeValue}${tempUnit}</span>
                        </div>
                        <div class="detail">
                            <i class="fas fa-tint"></i>
                            <span>Humidity: ${data.current.humidity}%</span>
                        </div>
                        <div class="detail">
                            <i class="fas fa-wind"></i>
                            <span>Wind: ${data.current.wind_speed} ${windUnit}</span>
                        </div>
                        <div class="detail">
                            <i class="fas fa-compress-arrows-alt"></i>
                            <span>Pressure: ${data.current.pressure} hPa</span>
                        </div>
                    </div>
                    <a href="/weather?lat=${lat}&lon=${lon}" class="btn btn-sm btn-primary view-more mt-2">View Details</a>
                </div>
            `;
            
            // Update popup with weather data
            loadingPopup.setContent(popupContent);
            
            // Store location in browser storage if it's a named location
            if (cityName) {
                storeRecentLocation(cityName, lat, lon);
            }
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            loadingPopup.setContent('<div class="text-danger"><i class="fas fa-exclamation-circle me-2"></i>Error loading weather data. Please try again.</div>');
        });
}

/**
 * Fetch weather specifically for city markers
 */
function fetchCityWeather(lat, lon, cityName, marker) {
    fetchLocationWeather(lat, lon, cityName, marker.getLatLng());
}

/**
 * Initialize current weather component
 */
function initCurrentWeather() {
    const locationParam = getLocationFromUrlParams();
    if (locationParam) {
        // Get weather for specific location
        if (locationParam.lat && locationParam.lon) {
            fetchWeatherData(locationParam.lat, locationParam.lon);
        } else if (locationParam.name) {
            geocodeLocation(locationParam.name)
                .then(location => {
                    if (location) {
                        fetchWeatherData(location.lat, location.lon);
                    }
                });
        }
    } else {
        // Try to get user's location
        getUserLocation()
            .then(userLocation => {
                fetchWeatherData(userLocation.lat, userLocation.lon);
            })
            .catch(() => {
                // Default to London if no location available
                fetchWeatherData(51.5074, -0.1278);
            });
    }
}

/**
 * Initialize forecast component
 */
function initForecast() {
    // This will be populated by initCurrentWeather
    // as it shares the same location data
}

/**
 * Get location from URL parameters
 */
function getLocationFromUrlParams() {
    const urlParams = new URLSearchParams(window.location.search);
    const lat = urlParams.get('lat');
    const lon = urlParams.get('lon');
    const location = urlParams.get('location');
    
    if (lat && lon) {
        return { lat: parseFloat(lat), lon: parseFloat(lon) };
    } else if (location) {
        return { name: location };
    }
    
    return null;
}

/**
 * Get user's current location
 */
function getUserLocation() {
    return new Promise((resolve, reject) => {
        // Try localStorage first (might have been set in base template)
        const storedLat = localStorage.getItem('userLat');
        const storedLon = localStorage.getItem('userLon');
        
        if (storedLat && storedLon) {
            resolve({ lat: parseFloat(storedLat), lon: parseFloat(storedLon) });
            return;
        }
        
        // Otherwise try geolocation API
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                position => {
                    const userLocation = {
                        lat: position.coords.latitude,
                        lon: position.coords.longitude
                    };
                    
                    // Store for future use
                    localStorage.setItem('userLat', userLocation.lat);
                    localStorage.setItem('userLon', userLocation.lon);
                    
                    resolve(userLocation);
                },
                error => {
                    console.warn('Geolocation error:', error);
                    reject(error);
                }
            );
        } else {
            reject(new Error('Geolocation not supported'));
        }
    });
}

/**
 * Geocode a location name to coordinates
 */
function geocodeLocation(locationName) {
    return fetch(`/api/geocode?location=${encodeURIComponent(locationName)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success && data.results && data.results.length > 0) {
                return data.results[0];
            }
            throw new Error('Location not found');
        });
}

/**
 * Fetch weather data for a location
 */
function fetchWeatherData(lat, lon, units = 'metric') {
    // Update loading state
    const weatherContainer = document.getElementById('current-weather');
    if (weatherContainer) {
        showLoading(weatherContainer, true);
    }
    
    // Fetch weather data
    return fetch(`/api/weather?lat=${lat}&lon=${lon}&units=${units}`)
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                throw new Error(data.message || 'Failed to fetch weather data');
            }
            
            // Store data in state
            weatherState.currentLocation = data.location;
            weatherState.weatherData = data.current;
            weatherState.units = units;
            
            // Update UI
            updateCurrentWeather(data);
            
            // Also fetch forecast
            return fetchForecastData(lat, lon, units);
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            
            // Show error
            if (weatherContainer) {
                showError(weatherContainer, 'Failed to fetch weather data. Please try again.');
            }
            
            throw error;
        });
}

/**
 * Fetch forecast data for a location
 */
function fetchForecastData(lat, lon, units = 'metric') {
    // Update loading state
    const forecastContainer = document.getElementById('forecast-container');
    if (forecastContainer) {
        forecastContainer.innerHTML = '<div class="col-12 text-center"><div class="spinner-border text-primary" role="status"></div></div>';
    }
    
    // Fetch forecast data
    return fetch(`/api/forecast?lat=${lat}&lon=${lon}&units=${units}`)
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                throw new Error(data.message || 'Failed to fetch forecast data');
            }
            
            // Store data in state
            weatherState.forecastData = data.forecast;
            
            // Update UI
            updateForecast(data);
            
            return data;
        })
        .catch(error => {
            console.error('Error fetching forecast data:', error);
            
            // Show error
            if (forecastContainer) {
                forecastContainer.innerHTML = '<div class="col-12"><div class="alert alert-danger">Failed to fetch forecast data. Please try again.</div></div>';
            }
            
            throw error;
        });
}

/**
 * Update current weather UI with data
 */
function updateCurrentWeather(data) {
    const current = data.current;
    const location = data.location;
    
    // Update location and time
    const locationNameElement = document.querySelector('.location-name');
    if (locationNameElement) {
        locationNameElement.textContent = `${location.name}, ${location.country}`;
    }
    
    const currentDatetimeElement = document.querySelector('.current-datetime');
    if (currentDatetimeElement) {
        const datetime = new Date(current.dt * 1000);
        currentDatetimeElement.textContent = datetime.toLocaleString();
    }
    
    // Update temperature and weather description
    const temperatureElement = document.querySelector('.temperature');
    if (temperatureElement) {
        const unit = weatherState.units === 'metric' ? '°C' : '°F';
        temperatureElement.textContent = `${Math.round(current.temp)}${unit}`;
    }
    
    const weatherDescriptionElement = document.querySelector('.weather-description');
    if (weatherDescriptionElement) {
        weatherDescriptionElement.textContent = current.weather.description;
    }
    
    const feelsLikeElement = document.querySelector('.feels-like .value');
    if (feelsLikeElement) {
        const unit = weatherState.units === 'metric' ? '°C' : '°F';
        feelsLikeElement.textContent = `${Math.round(current.feels_like)}${unit}`;
    }
    
    // Update weather icon
    const weatherIconElement = document.querySelector('.weather-icon i');
    if (weatherIconElement) {
        const iconClass = getWeatherIconClass(current.weather.id, current.dt, current.sunrise, current.sunset);
        
        // Remove all existing icon classes
        weatherIconElement.className = '';
        
        // Add new icon class
        weatherIconElement.classList.add('fas', iconClass, 'fa-4x');
    }
    
    // Update weather details
    const humidityElement = document.querySelector('.humidity .value');
    if (humidityElement) {
        humidityElement.textContent = `${current.humidity}%`;
    }
    
    const windElement = document.querySelector('.wind .value');
    if (windElement) {
        const unit = weatherState.units === 'metric' ? 'm/s' : 'mph';
        windElement.textContent = `${current.wind_speed} ${unit}`;
    }
    
    const pressureElement = document.querySelector('.pressure .value');
    if (pressureElement) {
        pressureElement.textContent = `${current.pressure} hPa`;
    }
    
    const visibilityElement = document.querySelector('.visibility .value');
    if (visibilityElement) {
        const visibilityKm = current.visibility / 1000;
        visibilityElement.textContent = `${visibilityKm.toFixed(1)} km`;
    }
}

/**
 * Update forecast UI with data
 */
function updateForecast(data) {
    const forecastContainer = document.getElementById('forecast-container');
    if (!forecastContainer) return;
    
    // Clear existing forecast
    forecastContainer.innerHTML = '';
    
    // Create forecast cards
    data.forecast.forEach(day => {
        const date = new Date(day.dt * 1000);
        const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
        const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        
        const unit = weatherState.units === 'metric' ? '°C' : '°F';
        const iconClass = getWeatherIconClass(day.weather.id);
        
        const forecastCard = document.createElement('div');
        forecastCard.className = 'col-md-6 col-lg-3 mb-4';
        forecastCard.innerHTML = `
            <div class="card h-100 weather-card">
                <div class="card-body text-center">
                    <h5 class="card-title">${dayName}, ${dateStr}</h5>
                    <div class="my-3">
                        <i class="fas ${iconClass} fa-3x text-primary"></i>
                    </div>
                    <div class="temperature-range d-flex justify-content-center align-items-center">
                        <span class="h3 mb-0 me-2">${Math.round(day.temp_max)}${unit}</span>
                        <span class="text-muted">${Math.round(day.temp_min)}${unit}</span>
                    </div>
                    <p class="mt-2 mb-0">${day.weather.description}</p>
                    <div class="mt-3 d-flex justify-content-around">
                        <div>
                            <i class="fas fa-tint text-primary"></i>
                            <span>${Math.round(day.humidity_avg)}%</span>
                        </div>
                        <div>
                            <i class="fas fa-wind text-primary"></i>
                            <span>${day.wind_speed_avg.toFixed(1)} ${weatherState.units === 'metric' ? 'm/s' : 'mph'}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        forecastContainer.appendChild(forecastCard);
    });
}

/**
 * Get weather icon class based on weather ID
 */
function getWeatherIconClass(weatherId, dt, sunrise, sunset) {
    // Check if it's night time
    let isNight = false;
    if (dt && sunrise && sunset) {
        isNight = dt < sunrise || dt > sunset;
    }
    
    // Weather icon mapping
    // https://openweathermap.org/weather-conditions
    
    // Thunderstorm: 200-299
    if (weatherId >= 200 && weatherId < 300) {
        return 'fa-bolt';
    }
    
    // Drizzle: 300-399
    if (weatherId >= 300 && weatherId < 400) {
        return 'fa-cloud-rain';
    }
    
    // Rain: 500-599
    if (weatherId >= 500 && weatherId < 600) {
        return weatherId >= 511 ? 'fa-cloud-showers-heavy' : 'fa-cloud-rain';
    }
    
    // Snow: 600-699
    if (weatherId >= 600 && weatherId < 700) {
        return 'fa-snowflake';
    }
    
    // Atmosphere (fog, mist, etc): 700-799
    if (weatherId >= 700 && weatherId < 800) {
        return 'fa-smog';
    }
    
    // Clear: 800
    if (weatherId === 800) {
        return isNight ? 'fa-moon' : 'fa-sun';
    }
    
    // Clouds: 801-899
    if (weatherId > 800 && weatherId < 900) {
        if (weatherId === 801) {
            return isNight ? 'fa-cloud-moon' : 'fa-cloud-sun';
        }
        return 'fa-cloud';
    }
    
    // Default
    return 'fa-cloud';
}

/**
 * Toggle temperature units between celsius and fahrenheit
 */
function toggleUnit(isFahrenheit) {
    // Always update units state, even if we don't have current location
    weatherState.units = isFahrenheit ? 'imperial' : 'metric';
    
    // If we don't have a location yet, just store the unit preference
    if (!weatherState.currentLocation) return;
    
    // Update popup display if a popup is open on the map
    if (window.map && window.map._popup) {
        // Re-fetch weather data for the current popup
        const latlng = window.map._popup._latlng;
        if (latlng) {
            fetchLocationWeather(latlng.lat, latlng.lng, null, latlng);
        }
    }
    
    // Fetch weather with new units for the main weather display
    fetchWeatherData(
        weatherState.currentLocation.lat, 
        weatherState.currentLocation.lon, 
        weatherState.units
    );
}

/**
 * Show loading state in container
 */
function showLoading(container, isLoading) {
    if (isLoading) {
        container.classList.add('loading');
        container.innerHTML = `
            <div class="loading-container">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
    } else {
        container.classList.remove('loading');
    }
}

/**
 * Show error message in container
 */
function showError(container, message) {
    container.innerHTML = `
        <div class="error-container">
            <i class="fas fa-exclamation-circle fa-2x mb-3"></i>
            <p>${message}</p>
        </div>
    `;
}

/**
 * Store a recently visited location
 */
function storeRecentLocation(name, lat, lon) {
    try {
        let recentLocations = JSON.parse(localStorage.getItem('recentLocations')) || [];
        
        // Check if location already exists
        const exists = recentLocations.some(loc => loc.name === name);
        
        if (!exists) {
            // Add to beginning of array
            recentLocations.unshift({ name, lat, lon });
            
            // Keep only the most recent 5
            if (recentLocations.length > 5) {
                recentLocations = recentLocations.slice(0, 5);
            }
            
            // Save back to localStorage
            localStorage.setItem('recentLocations', JSON.stringify(recentLocations));
        }
    } catch (error) {
        console.error('Error storing recent location:', error);
    }
}
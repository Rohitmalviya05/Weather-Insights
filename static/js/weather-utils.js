/**
 * Weather Insights - Utility Functions
 */

// Format temperature with unit
function formatTemperature(temp, unit = 'C') {
    const roundedTemp = Math.round(temp);
    return `${roundedTemp}°${unit}`;
}

// Format wind speed with unit
function formatWindSpeed(speed, unit = 'm/s') {
    if (unit === 'km/h') {
        return `${Math.round(speed * 3.6)} km/h`;
    } else if (unit === 'mph') {
        return `${Math.round(speed * 2.237)} mph`;
    }
    return `${speed} m/s`;
}

// Format time from timestamp
function formatTime(timestamp, timezone = 0, format = '24h') {
    const date = new Date((timestamp + timezone) * 1000);
    let hours = date.getUTCHours();
    const minutes = date.getUTCMinutes().toString().padStart(2, '0');
    
    if (format === '12h') {
        const period = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // Convert 0 to 12
        return `${hours}:${minutes} ${period}`;
    }
    
    return `${hours.toString().padStart(2, '0')}:${minutes}`;
}

// Format date from timestamp
function formatDate(timestamp, timezone = 0, format = 'short') {
    const date = new Date((timestamp + timezone) * 1000);
    
    const options = {
        weekday: format === 'full' ? 'long' : 'short',
        month: format === 'full' ? 'long' : 'short',
        day: 'numeric'
    };
    
    if (format === 'full') {
        options.year = 'numeric';
    }
    
    return date.toLocaleDateString('en-US', options);
}

// Get weather icon class based on condition and time
function getWeatherIconClass(condition, isDay = true) {
    // Default icon
    let iconClass = 'fas fa-cloud';
    
    // Map condition to Font Awesome icons
    const iconMap = {
        'clear': isDay ? 'fas fa-sun' : 'fas fa-moon',
        'clouds': 'fas fa-cloud',
        'few clouds': isDay ? 'fas fa-cloud-sun' : 'fas fa-cloud-moon',
        'scattered clouds': 'fas fa-cloud',
        'broken clouds': 'fas fa-cloud',
        'shower rain': 'fas fa-cloud-showers-heavy',
        'rain': 'fas fa-cloud-rain',
        'thunderstorm': 'fas fa-bolt',
        'snow': 'fas fa-snowflake',
        'mist': 'fas fa-smog',
        'fog': 'fas fa-smog',
        'haze': 'fas fa-smog',
        'dust': 'fas fa-smog',
        'smoke': 'fas fa-smog',
    };
    
    // Convert condition to lowercase for case-insensitive matching
    const conditionLower = condition.toLowerCase();
    
    // Find matching icon
    for (const [key, value] of Object.entries(iconMap)) {
        if (conditionLower.includes(key)) {
            iconClass = value;
            break;
        }
    }
    
    return iconClass;
}

// Get color class based on temperature
function getTemperatureColorClass(temp) {
    if (temp < 0) return 'text-info';
    if (temp < 10) return 'text-primary';
    if (temp < 20) return 'text-success';
    if (temp < 30) return 'text-warning';
    return 'text-danger';
}

// Get UV index description and color
function getUVIndexInfo(uvIndex) {
    let description, colorClass;
    
    if (uvIndex < 3) {
        description = 'Low';
        colorClass = 'text-success';
    } else if (uvIndex < 6) {
        description = 'Moderate';
        colorClass = 'text-warning';
    } else if (uvIndex < 8) {
        description = 'High';
        colorClass = 'text-orange';
    } else if (uvIndex < 11) {
        description = 'Very High';
        colorClass = 'text-danger';
    } else {
        description = 'Extreme';
        colorClass = 'text-purple';
    }
    
    return { description, colorClass };
}

// Get air quality description and color
function getAirQualityInfo(aqi) {
    let description, colorClass;
    
    if (aqi < 50) {
        description = 'Good';
        colorClass = 'text-success';
    } else if (aqi < 100) {
        description = 'Moderate';
        colorClass = 'text-warning';
    } else if (aqi < 150) {
        description = 'Unhealthy for Sensitive Groups';
        colorClass = 'text-orange';
    } else if (aqi < 200) {
        description = 'Unhealthy';
        colorClass = 'text-danger';
    } else if (aqi < 300) {
        description = 'Very Unhealthy';
        colorClass = 'text-purple';
    } else {
        description = 'Hazardous';
        colorClass = 'text-dark';
    }
    
    return { description, colorClass };
}

// Get direction from wind degrees
function getWindDirection(degrees) {
    const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
    const index = Math.round(degrees / 22.5) % 16;
    return directions[index];
}

// Create a weather card for a location
function createWeatherCard(weather, options = {}) {
    const defaultOptions = {
        showDetails: true,
        showForecast: false,
        temperatureUnit: 'C',
        windUnit: 'm/s'
    };
    
    const settings = { ...defaultOptions, ...options };
    
    // Extract data from weather object
    const temp = Math.round(weather.main.temp);
    const feelsLike = Math.round(weather.main.feels_like);
    const humidity = weather.main.humidity;
    const pressure = weather.main.pressure;
    const windSpeed = weather.wind.speed;
    const windDeg = weather.wind.deg;
    const condition = weather.weather[0].main;
    const description = weather.weather[0].description;
    const iconCode = weather.weather[0].icon;
    const isDay = iconCode.includes('d');
    const cityName = weather.name;
    const country = weather.sys.country;
    
    // Create card HTML
    const cardHTML = `
        <div class="weather-card card border-0 shadow-sm h-100">
            <div class="card-body">
                <div class="d-flex align-items-center mb-3">
                    <i class="${getWeatherIconClass(condition, isDay)} me-2 fs-3 ${getTemperatureColorClass(temp)}"></i>
                    <h5 class="card-title mb-0">${cityName}, ${country}</h5>
                </div>
                
                <div class="text-center my-3">
                    <div class="display-4 ${getTemperatureColorClass(temp)}">${formatTemperature(temp, settings.temperatureUnit)}</div>
                    <div class="text-muted">${description}</div>
                    <div class="mt-2">Feels like: ${formatTemperature(feelsLike, settings.temperatureUnit)}</div>
                </div>
                
                ${settings.showDetails ? `
                <div class="row mt-4">
                    <div class="col-6 mb-3">
                        <div class="d-flex align-items-center">
                            <i class="fas fa-wind me-2"></i>
                            <div>
                                <div class="small text-muted">Wind</div>
                                <div>${formatWindSpeed(windSpeed, settings.windUnit)} ${getWindDirection(windDeg)}</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-6 mb-3">
                        <div class="d-flex align-items-center">
                            <i class="fas fa-tint me-2"></i>
                            <div>
                                <div class="small text-muted">Humidity</div>
                                <div>${humidity}%</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-6 mb-3">
                        <div class="d-flex align-items-center">
                            <i class="fas fa-compress-alt me-2"></i>
                            <div>
                                <div class="small text-muted">Pressure</div>
                                <div>${pressure} hPa</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-6 mb-3">
                        <div class="d-flex align-items-center">
                            <i class="fas fa-sun me-2"></i>
                            <div>
                                <div class="small text-muted">Condition</div>
                                <div>${condition}</div>
                            </div>
                        </div>
                    </div>
                </div>
                ` : ''}
            </div>
        </div>
    `;
    
    return cardHTML;
}

// Get current location using browser geolocation
function getCurrentLocation() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                position => {
                    resolve({
                        lat: position.coords.latitude,
                        lon: position.coords.longitude
                    });
                },
                error => {
                    console.error('Geolocation error:', error);
                    reject(error);
                },
                { timeout: 10000 }
            );
        } else {
            reject(new Error('Geolocation is not supported by this browser'));
        }
    });
}
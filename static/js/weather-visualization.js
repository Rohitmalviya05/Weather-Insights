// Weather Visualization Module
// Handles visualizations for current weather, forecasts, and historical trends

// Store chart instances to destroy and recreate when needed
let temperatureChart = null;
let precipitationChart = null;
let historicalChart = null;

/**
 * Show loading indicators
 */
function showLoading() {
    const loadingElem = document.getElementById('weatherLoading');
    const contentElem = document.getElementById('weatherContent');
    const errorElem = document.getElementById('weatherError');
    
    if (loadingElem) loadingElem.classList.remove('d-none');
    if (contentElem) contentElem.classList.add('d-none');
    if (errorElem) errorElem.classList.add('d-none');
}

/**
 * Hide loading indicators
 */
function hideLoading() {
    const loadingElem = document.getElementById('weatherLoading');
    
    if (loadingElem) loadingElem.classList.add('d-none');
}

/**
 * Show weather content
 */
function showWeatherContent() {
    const contentElem = document.getElementById('weatherContent');
    
    if (contentElem) contentElem.classList.remove('d-none');
}

/**
 * Show error message
 */
function showError(message) {
    const errorElem = document.getElementById('weatherError');
    
    if (errorElem) {
        errorElem.textContent = message;
        errorElem.classList.remove('d-none');
    }
}

/**
 * Fetch weather data for the specified location
 * @param {string} location - The location to fetch weather for
 */
function fetchWeatherData(location) {
    showLoading();
    
    // Default to London if location is empty
    if (!location) {
        location = "London";
    }
    
    // Fetch coordinates for location
    fetch(`/api/geocode?location=${encodeURIComponent(location)}`)
        .then(response => response.json())
        .then(geoData => {
            if (geoData.success) {
                const lat = geoData.lat;
                const lon = geoData.lon;
                
                // Fetch current weather
                fetch(`/api/weather?lat=${lat}&lon=${lon}`)
                    .then(response => response.json())
                    .then(weatherData => {
                        if (weatherData.success) {
                            updateCurrentWeather(weatherData);
                            
                            // Fetch forecast
                            fetch(`/api/forecast?lat=${lat}&lon=${lon}`)
                                .then(response => response.json())
                                .then(forecastData => {
                                    if (forecastData.success) {
                                        updateForecastWeather(forecastData);
                                    }
                                    
                                    // Get historical data
                                    fetch(`/api/historical?lat=${lat}&lon=${lon}`)
                                        .then(response => response.json())
                                        .then(historicalData => {
                                            if (historicalData.success) {
                                                updateHistoricalTrends(historicalData);
                                            }
                                            
                                            hideLoading();
                                            showWeatherContent();
                                        })
                                        .catch(error => {
                                            console.error('Error fetching historical data:', error);
                                            hideLoading();
                                            showWeatherContent();
                                        });
                                })
                                .catch(error => {
                                    console.error('Error fetching forecast:', error);
                                    hideLoading();
                                    showWeatherContent();
                                });
                        } else {
                            // Show error message from weather service
                            hideLoading();
                            showError(weatherData.message || 'Failed to fetch weather data');
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching current weather:', error);
                        hideLoading();
                        showError('Failed to fetch weather data. Please try again later.');
                    });
            } else {
                console.error('Location not found');
                hideLoading();
                showError('Location not found. Please try a different city or location.');
            }
        })
        .catch(error => {
            console.error('Error geocoding location:', error);
            hideLoading();
            showError('Error finding location. Please try again.');
        });
}

/**
 * Update the current weather display with the provided data
 * @param {Object} data - The current weather data
 */
function updateCurrentWeather(data) {
    if (!data.success) {
        showError('Unable to fetch current weather data');
        return;
    }
    
    const currentWeather = data.current;
    
    // Update location and time
    const locationElement = document.getElementById('weatherLocation');
    if (locationElement) locationElement.textContent = data.location;
    
    const dateTimeElement = document.getElementById('weatherDateTime');
    if (dateTimeElement) dateTimeElement.textContent = currentWeather.datetime;
    
    // Update temperature
    const currentTempElement = document.getElementById('currentTemp');
    if (currentTempElement) currentTempElement.textContent = `${Math.round(currentWeather.temp)}°C`;
    
    const feelsLikeElement = document.getElementById('feelsLike');
    if (feelsLikeElement) feelsLikeElement.textContent = `Feels like: ${Math.round(currentWeather.feels_like)}°C`;
    
    // Update weather condition
    const weatherCondElement = document.getElementById('weatherCondition');
    if (weatherCondElement) weatherCondElement.textContent = currentWeather.description;
    
    // Update weather icon
    const weatherIconElement = document.getElementById('weatherIcon');
    if (weatherIconElement) {
        weatherIconElement.className = '';
        weatherIconElement.classList.add('fas', currentWeather.icon_class.split(' ')[0], 'display-1', 'text-light');
    }
    
    // Update details
    const windInfoElement = document.getElementById('windInfo');
    if (windInfoElement) windInfoElement.textContent = `${currentWeather.wind_speed} km/h`;
    
    const humidityInfoElement = document.getElementById('humidityInfo');
    if (humidityInfoElement) humidityInfoElement.textContent = `${currentWeather.humidity}%`;
    
    const pressureInfoElement = document.getElementById('pressureInfo');
    if (pressureInfoElement) pressureInfoElement.textContent = `${currentWeather.pressure} hPa`;
    
    const uvInfoElement = document.getElementById('uvInfo');
    if (uvInfoElement && currentWeather.uv_index !== undefined) {
        uvInfoElement.textContent = currentWeather.uv_index;
    }
    
    // Create chart for today's temperature if Chart.js is loaded
    if (typeof Chart !== 'undefined' && currentWeather.hourly_forecast) {
        createTemperatureChart(currentWeather.hourly_forecast);
    }
}

/**
 * Update the forecast weather display with the provided data
 * @param {Object} data - The forecast weather data
 */
function updateForecastWeather(data) {
    if (!data.success) {
        console.error('Unable to fetch forecast data');
        return;
    }
    
    const forecastContainer = document.getElementById('forecastContainer');
    if (!forecastContainer) return;
    
    forecastContainer.innerHTML = '';
    
    // Create forecast cards
    data.forecast.forEach((day, index) => {
        if (index < 7) { // Only show 7 days
            const card = document.createElement('div');
            card.className = 'col-md-auto col-6 mb-3';
            
            // Format date
            const date = new Date(day.date);
            const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
            const dayNum = date.getDate();
            
            card.innerHTML = `
                <div class="forecast-day shadow-sm">
                    <h6 class="card-title mb-1">${dayName} ${dayNum}</h6>
                    <i class="fas ${day.icon} text-primary my-2" style="font-size: 24px;"></i>
                    <div class="temp-range">
                        <span class="high-temp">${Math.round(day.temp.max)}°</span>
                        <span class="low-temp text-muted">${Math.round(day.temp.min)}°</span>
                    </div>
                    <div class="small text-muted mt-1">${day.description}</div>
                </div>
            `;
            
            forecastContainer.appendChild(card);
        }
    });
    
    // Create forecast charts if Chart.js is loaded
    if (typeof Chart !== 'undefined') {
        createForecastCharts(data.forecast);
    }
}

/**
 * Update the historical trends display with the provided data
 * @param {Object} data - The historical trends data
 */
function updateHistoricalTrends(data) {
    if (!data.success) {
        console.error('Unable to fetch historical data');
        return;
    }
    
    // Create historical chart if Chart.js is loaded
    if (typeof Chart !== 'undefined') {
        createHistoricalChart(data);
    }
}

/**
 * Create temperature chart for current day
 * @param {Array} hourlyData - Hourly forecast data for today
 */
function createTemperatureChart(hourlyData) {
    const canvas = document.getElementById('todayTemperatureChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart if it exists
    if (temperatureChart) {
        temperatureChart.destroy();
    }
    
    const labels = hourlyData.map(hour => hour.time);
    const temperatures = hourlyData.map(hour => hour.temp);
    
    temperatureChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Temperature (°C)',
                data: temperatures,
                borderColor: '#4361ee',
                backgroundColor: 'rgba(67, 97, 238, 0.1)',
                borderWidth: 2,
                pointBackgroundColor: '#4361ee',
                pointRadius: 3,
                pointHoverRadius: 5,
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Today\'s Temperature Forecast',
                    font: {
                        size: 16,
                        weight: 'normal'
                    },
                    padding: 20
                }
            }
        }
    });
}

/**
 * Create forecast charts
 * @param {Array} forecastData - Forecast data for the next days
 */
function createForecastCharts(forecastData) {
    // Temperature forecast chart
    const tempCanvas = document.getElementById('forecastTemperatureChart');
    if (!tempCanvas) return;
    
    const tempCtx = tempCanvas.getContext('2d');
    
    // Destroy existing chart if it exists
    if (temperatureChart) {
        temperatureChart.destroy();
    }
    
    const labels = forecastData.slice(0, 7).map(day => {
        const date = new Date(day.date);
        return date.toLocaleDateString('en-US', { weekday: 'short' });
    });
    
    const maxTemps = forecastData.slice(0, 7).map(day => day.temp.max);
    const minTemps = forecastData.slice(0, 7).map(day => day.temp.min);
    
    temperatureChart = new Chart(tempCtx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Max Temperature (°C)',
                    data: maxTemps,
                    backgroundColor: 'rgba(255, 99, 132, 0.7)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Min Temperature (°C)',
                    data: minTemps,
                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: '7-Day Temperature Forecast',
                    font: {
                        size: 16,
                        weight: 'normal'
                    },
                    padding: 20
                }
            }
        }
    });
    
    // Precipitation forecast chart
    const precipCanvas = document.getElementById('forecastPrecipitationChart');
    if (!precipCanvas) return;
    
    const precipCtx = precipCanvas.getContext('2d');
    
    // Destroy existing chart if it exists
    if (precipitationChart) {
        precipitationChart.destroy();
    }
    
    const precipitation = forecastData.slice(0, 7).map(day => day.precipitation_chance || 0);
    
    precipitationChart = new Chart(precipCtx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Precipitation (%)',
                    data: precipitation,
                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: '7-Day Precipitation Forecast',
                    font: {
                        size: 16,
                        weight: 'normal'
                    },
                    padding: 20
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

/**
 * Create historical chart
 * @param {Object} data - Historical data
 */
function createHistoricalChart(data) {
    const canvas = document.getElementById('historicalTrendsChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart if it exists
    if (historicalChart) {
        historicalChart.destroy();
    }
    
    const dates = data.data.map(item => item.date);
    const temps = data.data.map(item => item.temp);
    
    historicalChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: temps,
                    borderColor: '#4361ee',
                    backgroundColor: 'rgba(67, 97, 238, 0.1)',
                    borderWidth: 2,
                    pointBackgroundColor: '#4361ee',
                    pointRadius: 3,
                    pointHoverRadius: 5,
                    fill: true,
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: '30-Day Temperature Trends',
                    font: {
                        size: 16,
                        weight: 'normal'
                    },
                    padding: 20
                }
            }
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Set up search form
    const searchForm = document.querySelector('form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const locationInput = document.querySelector('input[name="location"]');
            if (locationInput) {
                const location = locationInput.value.trim();
                if (location) {
                    // If we're on the weather page with a form, let the form submit naturally
                    if (window.location.pathname.includes('/weather')) {
                        return true;
                    }
                    
                    // Otherwise prevent default and redirect
                    e.preventDefault();
                    window.location.href = `/weather?location=${encodeURIComponent(location)}`;
                }
            }
        });
    }
    
    // If we're on the weather page, get the location from the URL
    if (window.location.pathname.includes('/weather')) {
        const urlParams = new URLSearchParams(window.location.search);
        const location = urlParams.get('location');
        
        // Load weather data
        fetchWeatherData(location);
    }
});
/**
 * Hyper-Local Weather Forecast page functionality
 */
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const addressInput = document.getElementById('address-input');
    const locateMe = document.getElementById('locate-me');
    const addressSuggestions = document.getElementById('address-suggestions');
    const forecastContainer = document.getElementById('forecast-container');
    const noLocationContainer = document.getElementById('no-location-container');
    const mapLoading = document.getElementById('map-loading');
    
    // Map and location variables
    let map;
    let marker;
    let currentLat;
    let currentLng;
    
    // Initialize map
    function initializeMap() {
        // Create a placeholder map centered on a default location
        map = utils.initMap('forecast-map');
        
        // Add click event to map for selecting location
        map.on('click', function(e) {
            updateLocation(e.latlng.lat, e.latlng.lng);
            fetchForecast(e.latlng.lat, e.latlng.lng);
        });
        
        // Hide loading overlay after map is loaded
        map.on('load', function() {
            mapLoading.style.display = 'none';
        });
    }
    
    // Handle "Locate Me" button click
    locateMe.addEventListener('click', function() {
        locateMe.disabled = true;
        locateMe.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Locating...';
        
        utils.getCurrentLocation()
            .then(coords => {
                currentLat = coords.latitude;
                currentLng = coords.longitude;
                
                updateLocation(currentLat, currentLng);
                fetchForecast(currentLat, currentLng);
                
                // Attempt to get the address for the coordinates
                reverseGeocode(currentLat, currentLng)
                    .then(address => {
                        addressInput.value = address;
                    })
                    .catch(error => {
                        console.error('Error getting address:', error);
                        addressInput.value = `${currentLat.toFixed(4)}, ${currentLng.toFixed(4)}`;
                    });
            })
            .catch(error => {
                console.error('Error getting location:', error);
                alert(error.message || 'Failed to get your location. Please try entering an address.');
            })
            .finally(() => {
                locateMe.disabled = false;
                locateMe.innerHTML = '<i class="fas fa-crosshairs me-2"></i>My Location';
            });
    });
    
    // Handle address input for autocomplete
    addressInput.addEventListener('input', utils.debounce(function() {
        const query = this.value.trim();
        
        if (query.length < 3) {
            addressSuggestions.style.display = 'none';
            return;
        }
        
        // In a real implementation, this would call a geocoding API
        // For demo, show some sample suggestions
        showSampleSuggestions(query);
    }, 300));
    
    // Create map when the page loads
    initializeMap();
    
    /**
     * Update map location and marker
     * @param {number} lat - Latitude
     * @param {number} lng - Longitude
     */
    function updateLocation(lat, lng) {
        currentLat = lat;
        currentLng = lng;
        
        // Show the forecast container
        forecastContainer.style.display = 'block';
        noLocationContainer.style.display = 'none';
        
        // Update map view
        map.setView([lat, lng], 13);
        
        // Update or create marker
        if (marker) {
            marker.setLatLng([lat, lng]);
        } else {
            marker = utils.createMapMarker(map, lat, lng, {
                draggable: true,
                title: 'Weather location'
            });
            
            // Update forecast when marker is dragged
            marker.on('dragend', function() {
                const pos = this.getLatLng();
                currentLat = pos.lat;
                currentLng = pos.lng;
                fetchForecast(currentLat, currentLng);
                
                // Update address input
                reverseGeocode(currentLat, currentLng)
                    .then(address => {
                        addressInput.value = address;
                    })
                    .catch(error => {
                        console.error('Error getting address:', error);
                        addressInput.value = `${currentLat.toFixed(4)}, ${currentLng.toFixed(4)}`;
                    });
            });
        }
    }
    
    /**
     * Fetch weather forecast for given coordinates
     * @param {number} lat - Latitude
     * @param {number} lng - Longitude
     */
    function fetchForecast(lat, lng) {
        // Show loading indicators
        document.getElementById('minute-forecast').innerHTML = loadingSpinner();
        document.getElementById('hourly-forecast').innerHTML = loadingSpinner();
        document.getElementById('current-conditions').innerHTML = loadingSpinner();
        document.getElementById('daily-forecast').innerHTML = loadingSpinner();
        
        // In a real implementation, this would call a weather API
        // For demo, simulate loading time then show sample data
        setTimeout(() => {
            displayCurrentConditions();
            displayMinuteForecast();
            displayHourlyForecast();
            displayDailyForecast();
        }, 1500);
    }
    
    /**
     * Perform reverse geocoding to get address from coordinates
     * @param {number} lat - Latitude
     * @param {number} lng - Longitude
     * @returns {Promise} Promise resolving to address string
     */
    function reverseGeocode(lat, lng) {
        // In a real implementation, this would call a geocoding API
        // For demo, return a placeholder
        return Promise.resolve('Sample Location');
    }
    
    /**
     * Show sample address suggestions
     * @param {string} query - Search query
     */
    function showSampleSuggestions(query) {
        const sampleAddresses = [
            'Central Park, New York, NY',
            'Times Square, New York, NY',
            'Empire State Building, New York, NY',
            'Brooklyn Bridge, New York, NY',
            'Statue of Liberty, New York, NY'
        ];
        
        const filteredAddresses = sampleAddresses.filter(address => 
            address.toLowerCase().includes(query.toLowerCase())
        );
        
        if (filteredAddresses.length > 0) {
            addressSuggestions.innerHTML = '';
            
            filteredAddresses.forEach(address => {
                const item = document.createElement('div');
                item.className = 'address-suggestion-item';
                item.textContent = address;
                
                item.addEventListener('click', function() {
                    addressInput.value = address;
                    addressSuggestions.style.display = 'none';
                    
                    // In a real implementation, geocode the address to get coordinates
                    // For demo, use random coordinates near New York
                    const lat = 40.7128 + (Math.random() - 0.5) * 0.1;
                    const lng = -74.0060 + (Math.random() - 0.5) * 0.1;
                    
                    updateLocation(lat, lng);
                    fetchForecast(lat, lng);
                });
                
                addressSuggestions.appendChild(item);
            });
            
            addressSuggestions.style.display = 'block';
        } else {
            addressSuggestions.style.display = 'none';
        }
    }
    
    /**
     * Display current weather conditions
     */
    function displayCurrentConditions() {
        const currentConditionsElement = document.getElementById('current-conditions');
        
        // Sample current conditions data
        const current = {
            temperature: 24,
            feelsLike: 26,
            humidity: 65,
            windSpeed: 12,
            windDirection: 'NE',
            description: 'Partly Cloudy',
            icon: 'fas fa-cloud-sun'
        };
        
        currentConditionsElement.innerHTML = `
            <div class="text-center mb-4">
                <i class="${current.icon} fa-4x text-primary mb-3"></i>
                <h2 class="temperature mb-0">${utils.formatTemperature(current.temperature)}</h2>
                <p class="description text-muted">${current.description}</p>
            </div>
            
            <div class="row g-0">
                <div class="col-6 p-2">
                    <div class="d-flex align-items-center">
                        <i class="fas fa-thermometer-half text-primary me-2"></i>
                        <div>
                            <div class="text-muted small">Feels Like</div>
                            <div>${utils.formatTemperature(current.feelsLike)}</div>
                        </div>
                    </div>
                </div>
                <div class="col-6 p-2">
                    <div class="d-flex align-items-center">
                        <i class="fas fa-tint text-primary me-2"></i>
                        <div>
                            <div class="text-muted small">Humidity</div>
                            <div>${current.humidity}%</div>
                        </div>
                    </div>
                </div>
                <div class="col-6 p-2">
                    <div class="d-flex align-items-center">
                        <i class="fas fa-wind text-primary me-2"></i>
                        <div>
                            <div class="text-muted small">Wind</div>
                            <div>${current.windSpeed} km/h ${current.windDirection}</div>
                        </div>
                    </div>
                </div>
                <div class="col-6 p-2">
                    <div class="d-flex align-items-center">
                        <i class="fas fa-sun text-primary me-2"></i>
                        <div>
                            <div class="text-muted small">UV Index</div>
                            <div>3 (Moderate)</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    /**
     * Display minute-by-minute precipitation forecast
     */
    function displayMinuteForecast() {
        const minuteForecastElement = document.getElementById('minute-forecast');
        
        // Generate sample minute forecast data (60 minutes)
        const minutes = [];
        let precipProbability = Math.random() * 0.7; // Initial probability
        
        for (let i = 0; i < 60; i += 5) {
            // Fluctuate precipitation probability for realism
            precipProbability += (Math.random() - 0.5) * 0.2;
            precipProbability = Math.max(0, Math.min(1, precipProbability));
            
            const time = new Date();
            time.setMinutes(time.getMinutes() + i);
            
            minutes.push({
                time: time,
                probability: precipProbability,
                intensity: precipProbability > 0.3 ? precipProbability * 2 : 0
            });
        }
        
        // Build the minute forecast HTML
        let minuteHTML = '';
        
        minutes.forEach(minute => {
            const height = Math.round(minute.intensity * 80);
            const timeLabel = i => (i === 0 ? 'Now' : `+${i}m`);
            
            minuteHTML += `
                <div class="minute-forecast">
                    <div class="minute-precip">
                        <div class="minute-precip-bar" style="height: ${height}px;"></div>
                    </div>
                    <div class="mt-2 small">${timeLabel(minute.time.getMinutes() - new Date().getMinutes())}</div>
                    <div class="small text-muted">${Math.round(minute.probability * 100)}%</div>
                </div>
            `;
        });
        
        // If no precipitation expected, show a message
        if (minutes.every(m => m.intensity === 0)) {
            minuteHTML = `
                <div class="alert alert-info w-100 text-center">
                    <i class="fas fa-check-circle me-2"></i>
                    No precipitation expected in the next hour
                </div>
            `;
        }
        
        minuteForecastElement.innerHTML = minuteHTML;
    }
    
    /**
     * Display hourly weather forecast
     */
    function displayHourlyForecast() {
        const hourlyForecastElement = document.getElementById('hourly-forecast');
        
        // Generate sample hourly forecast data (24 hours)
        const hours = [];
        let temp = 22 + (Math.random() - 0.5) * 5; // Initial temperature
        
        for (let i = 0; i < 24; i++) {
            // Fluctuate temperature for realism
            temp += (Math.random() - 0.5) * 2;
            if (i % 24 < 6) temp -= 0.5; // Cooler at night
            if (i % 24 > 10 && i % 24 < 16) temp += 0.5; // Warmer during day
            
            const time = new Date();
            time.setHours(time.getHours() + i);
            
            // Generate random weather conditions
            const conditions = ['clear', 'partly-cloudy', 'cloudy', 'rain', 'thunderstorm'];
            const condition = conditions[Math.floor(Math.random() * conditions.length)];
            
            // Determine icon based on condition
            let icon;
            switch (condition) {
                case 'clear':
                    icon = time.getHours() >= 6 && time.getHours() < 20 ? 'fas fa-sun' : 'fas fa-moon';
                    break;
                case 'partly-cloudy':
                    icon = time.getHours() >= 6 && time.getHours() < 20 ? 'fas fa-cloud-sun' : 'fas fa-cloud-moon';
                    break;
                case 'cloudy':
                    icon = 'fas fa-cloud';
                    break;
                case 'rain':
                    icon = 'fas fa-cloud-rain';
                    break;
                case 'thunderstorm':
                    icon = 'fas fa-bolt';
                    break;
                default:
                    icon = 'fas fa-cloud';
            }
            
            hours.push({
                time: time,
                temperature: temp,
                icon: icon,
                precipProbability: condition === 'rain' || condition === 'thunderstorm' ? Math.random() * 0.8 + 0.2 : Math.random() * 0.2
            });
        }
        
        // Build the hourly forecast HTML
        let hourlyHTML = '';
        
        hours.forEach(hour => {
            const timeLabel = hour.time.getHours() === new Date().getHours() ? 'Now' : utils.formatTime(hour.time);
            
            hourlyHTML += `
                <div class="hourly-forecast">
                    <div class="small">${timeLabel}</div>
                    <div class="my-2">
                        <i class="${hour.icon} fa-lg"></i>
                    </div>
                    <div class="fw-bold">${utils.formatTemperature(hour.temperature)}</div>
                    <div class="precip-probability mt-1" title="${Math.round(hour.precipProbability * 100)}% chance of precipitation">
                        <div class="precip-probability-fill" style="width: ${hour.precipProbability * 100}%"></div>
                    </div>
                    <div class="mt-1 small text-muted">
                        <i class="fas fa-tint fa-sm"></i> ${Math.round(hour.precipProbability * 100)}%
                    </div>
                </div>
            `;
        });
        
        hourlyForecastElement.innerHTML = hourlyHTML;
    }
    
    /**
     * Display daily weather forecast
     */
    function displayDailyForecast() {
        const dailyForecastElement = document.getElementById('daily-forecast');
        
        // Generate sample daily forecast data (7 days)
        const days = [];
        let highTemp = 24 + (Math.random() - 0.5) * 8;
        let lowTemp = highTemp - 8 - (Math.random() * 4);
        
        for (let i = 0; i < 7; i++) {
            // Fluctuate temperatures for realism
            highTemp += (Math.random() - 0.5) * 3;
            lowTemp += (Math.random() - 0.5) * 2;
            
            const date = new Date();
            date.setDate(date.getDate() + i);
            
            // Generate random weather conditions
            const conditions = ['clear', 'partly-cloudy', 'cloudy', 'rain', 'thunderstorm'];
            const condition = conditions[Math.floor(Math.random() * conditions.length)];
            
            // Determine icon based on condition
            let icon;
            switch (condition) {
                case 'clear':
                    icon = 'fas fa-sun';
                    break;
                case 'partly-cloudy':
                    icon = 'fas fa-cloud-sun';
                    break;
                case 'cloudy':
                    icon = 'fas fa-cloud';
                    break;
                case 'rain':
                    icon = 'fas fa-cloud-rain';
                    break;
                case 'thunderstorm':
                    icon = 'fas fa-bolt';
                    break;
                default:
                    icon = 'fas fa-cloud';
            }
            
            days.push({
                date: date,
                highTemp: highTemp,
                lowTemp: lowTemp,
                condition: condition,
                icon: icon,
                precipProbability: condition === 'rain' || condition === 'thunderstorm' ? Math.random() * 0.8 + 0.2 : Math.random() * 0.2
            });
        }
        
        // Build the daily forecast HTML
        let dailyHTML = '';
        
        days.forEach((day, index) => {
            const dateLabel = index === 0 ? 'Today' : 
                              index === 1 ? 'Tomorrow' : 
                              utils.formatDate(day.date);
            
            dailyHTML += `
                <div class="daily-forecast">
                    <div class="daily-icon">
                        <i class="${day.icon}"></i>
                    </div>
                    <div>
                        <div class="fw-bold">${dateLabel}</div>
                        <div class="small text-muted">${day.condition.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}</div>
                    </div>
                    <div class="daily-temp-range">
                        <span class="daily-high">${utils.formatTemperature(day.highTemp)}</span>
                        <span class="mx-1">/</span>
                        <span class="daily-low">${utils.formatTemperature(day.lowTemp)}</span>
                    </div>
                </div>
            `;
        });
        
        dailyForecastElement.innerHTML = dailyHTML;
    }
    
    /**
     * Generate HTML for loading spinner
     * @returns {string} HTML string for loading spinner
     */
    function loadingSpinner() {
        return `
            <div class="text-center py-4 text-muted">
                <div class="spinner-border spinner-border-sm text-primary me-2" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                Loading forecast...
            </div>
        `;
    }
});

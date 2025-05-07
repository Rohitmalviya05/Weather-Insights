/**
 * Smart Weather Notifications page functionality
 */
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const locationInput = document.getElementById('location-input');
    const currentLocationBtn = document.getElementById('current-location-btn');
    const latitudeInput = document.getElementById('latitude');
    const longitudeInput = document.getElementById('longitude');
    const getNotificationsBtn = document.getElementById('get-notifications-btn');
    const smartNotificationsContainer = document.getElementById('smart-notifications-container');
    const noNotificationsContainer = document.getElementById('no-notifications-container');
    const notificationSettings = document.querySelectorAll('.form-check-input');
    
    // Check if Twilio credentials are available
    checkTwilioCredentials();
    
    /**
     * Check if Twilio credentials are available for SMS notifications
     */
    function checkTwilioCredentials() {
        fetch('/api/check-twilio-credentials')
            .then(response => response.json())
            .then(data => {
                if (!data.credentials_available) {
                    // Show warning if credentials are missing
                    const phoneVerificationSection = document.querySelector('.sms-alerts');
                    if (phoneVerificationSection) {
                        phoneVerificationSection.innerHTML = `
                            <div class="alert alert-warning">
                                <i class="fas fa-exclamation-triangle me-2"></i>
                                <span>SMS notifications are currently unavailable. Please check back later.</span>
                            </div>
                            <p class="text-muted">Weather alerts will still be available via email and browser notifications.</p>
                        `;
                    }
                    
                    // Disable SMS-related settings
                    const smsToggle = document.getElementById('alertSMS');
                    if (smsToggle) {
                        smsToggle.disabled = true;
                        smsToggle.checked = false;
                        const label = smsToggle.nextElementSibling;
                        if (label) {
                            label.classList.add('text-muted');
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Error checking Twilio credentials:', error);
            });
    
    // Map variables
    let map;
    let marker;
    
    // Initialize the map
    function initializeMap() {
        map = utils.initMap('notifications-map');
        
        // Add click event to map
        map.on('click', function(e) {
            updateLocation(e.latlng.lat, e.latlng.lng);
        });
    }
    
    // Initialize map when page loads
    initializeMap();
    
    // Handle current location button click
    currentLocationBtn.addEventListener('click', function() {
        currentLocationBtn.disabled = true;
        currentLocationBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
        
        utils.getCurrentLocation()
            .then(coords => {
                updateLocation(coords.latitude, coords.longitude);
                
                // Reverse geocode to get location name
                fetchLocationName(coords.latitude, coords.longitude)
                    .then(locationName => {
                        locationInput.value = locationName;
                    })
                    .catch(error => {
                        console.error('Error getting location name:', error);
                    })
                    .finally(() => {
                        currentLocationBtn.disabled = false;
                        currentLocationBtn.innerHTML = '<i class="fas fa-crosshairs"></i>';
                    });
            })
            .catch(error => {
                utils.showError('notifications-map', error.message);
                currentLocationBtn.disabled = false;
                currentLocationBtn.innerHTML = '<i class="fas fa-crosshairs"></i>';
            });
    });
    
    // Handle get notifications button click
    getNotificationsBtn.addEventListener('click', function() {
        const lat = latitudeInput.value;
        const lon = longitudeInput.value;
        
        if (!lat || !lon) {
            alert('Please select a location first');
            return;
        }
        
        // Get enabled notification types
        const enabledNotifications = [];
        notificationSettings.forEach(setting => {
            if (setting.checked) {
                enabledNotifications.push(setting.id.replace('setting-', ''));
            }
        });
        
        getNotificationsBtn.disabled = true;
        getNotificationsBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
        
        // Show the notifications container
        smartNotificationsContainer.style.display = 'block';
        noNotificationsContainer.style.display = 'none';
        
        // Fetch notifications
        generateSmartNotifications(lat, lon, enabledNotifications)
            .then(() => {
                getNotificationsBtn.disabled = false;
                getNotificationsBtn.innerHTML = 'Get Smart Notifications';
            })
            .catch(error => {
                console.error('Error generating notifications:', error);
                getNotificationsBtn.disabled = false;
                getNotificationsBtn.innerHTML = 'Get Smart Notifications';
            });
    });
    
    /**
     * Update location inputs and map marker
     * @param {number} lat - Latitude
     * @param {number} lon - Longitude
     */
    function updateLocation(lat, lon) {
        // Update hidden inputs
        latitudeInput.value = lat;
        longitudeInput.value = lon;
        
        // Update map view and marker
        map.setView([lat, lon], 13);
        
        if (marker) {
            marker.setLatLng([lat, lon]);
        } else {
            marker = utils.createMapMarker(map, lat, lon, {
                draggable: true,
                title: 'Your location'
            });
            
            // Update coordinates when marker is dragged
            marker.on('dragend', function() {
                const position = marker.getLatLng();
                updateLocation(position.lat, position.lng);
            });
        }
    }
    
    /**
     * Fetch location name from coordinates using reverse geocoding
     * @param {number} lat - Latitude
     * @param {number} lon - Longitude
     * @returns {Promise} Promise resolving to location name
     */
    function fetchLocationName(lat, lon) {
        // This would normally use a geocoding API
        // For demo purposes, return a placeholder
        return Promise.resolve('Selected Location');
    }
    
    /**
     * Generate smart notifications based on weather conditions
     * @param {number} lat - Latitude
     * @param {number} lon - Longitude
     * @param {Array} notificationTypes - Enabled notification types
     * @returns {Promise} Promise resolving when notifications are generated
     */
    function generateSmartNotifications(lat, lon, notificationTypes) {
        return new Promise((resolve) => {
            // This would normally fetch data from the API
            // For demo, let's simulate loading time and populate with sample data
            setTimeout(() => {
                // Update notifications summary
                document.getElementById('notifications-summary').textContent = 
                    'Based on your location and preferences, we\'ve generated the following smart weather notifications.';
                
                // Generate notifications list
                const notificationsList = document.getElementById('notifications-list');
                notificationsList.innerHTML = '';
                
                // Create category containers
                if (notificationTypes.includes('temperature')) {
                    const temperatureCategory = createNotificationCategory('Temperature Changes', 'temperature-high');
                    
                    // Add notifications to this category
                    temperatureCategory.appendChild(createNotification(
                        'low',
                        'temperature-high',
                        'Warming Trend',
                        'Temperature will rise by 5°C over the next 2 days, reaching a high of 26°C on Wednesday.'
                    ));
                    
                    notificationsList.appendChild(temperatureCategory);
                }
                
                if (notificationTypes.includes('precipitation')) {
                    const precipCategory = createNotificationCategory('Precipitation Alerts', 'cloud-rain');
                    
                    // Add notifications to this category
                    precipCategory.appendChild(createNotification(
                        'medium',
                        'cloud-rain',
                        'Rain Expected',
                        'There\'s a 70% chance of rain tomorrow afternoon from 2 PM to 6 PM.'
                    ));
                    
                    precipCategory.appendChild(createNotification(
                        'low',
                        'cloud-sun',
                        'Dry Period Ahead',
                        'Following tomorrow\'s rain, expect a dry period of at least 5 days.'
                    ));
                    
                    notificationsList.appendChild(precipCategory);
                }
                
                if (notificationTypes.includes('activities')) {
                    const activitiesCategory = createNotificationCategory('Outdoor Activities', 'hiking');
                    
                    // Add notifications to this category
                    activitiesCategory.appendChild(createNotification(
                        'high',
                        'sun',
                        'Perfect Weather Window',
                        'Thursday will have ideal conditions for outdoor activities with mild temperatures, low humidity, and gentle breeze.'
                    ));
                    
                    notificationsList.appendChild(activitiesCategory);
                }
                
                if (notificationTypes.includes('weekend')) {
                    const weekendCategory = createNotificationCategory('Weekend Forecast', 'calendar-alt');
                    
                    // Add notifications to this category
                    weekendCategory.appendChild(createNotification(
                        'medium',
                        'cloud-sun-rain',
                        'Mixed Weekend Weather',
                        'Saturday will be mostly sunny with a high of 24°C. Sunday has a 40% chance of scattered showers.'
                    ));
                    
                    notificationsList.appendChild(weekendCategory);
                }
                
                // If no categories were added, show a message
                if (notificationsList.children.length === 0) {
                    notificationsList.innerHTML = `
                        <div class="empty-notifications">
                            <i class="fas fa-bell-slash fa-2x mb-3"></i>
                            <h5>No Notifications Available</h5>
                            <p class="mb-0">Please enable at least one notification type in your preferences.</p>
                        </div>
                    `;
                }
                
                resolve();
            }, 1500);
        });
    }
    
    /**
     * Create a notification category element
     * @param {string} title - Category title
     * @param {string} icon - Category icon name
     * @returns {HTMLElement} Category element
     */
    function createNotificationCategory(title, icon) {
        const categoryDiv = document.createElement('div');
        categoryDiv.className = 'notification-category';
        
        categoryDiv.innerHTML = `
            <div class="d-flex align-items-center mb-3">
                <div class="category-icon">
                    <i class="fas fa-${icon}"></i>
                </div>
                <h4 class="mb-0">${title}</h4>
            </div>
        `;
        
        return categoryDiv;
    }
    
    /**
     * Create a notification element
     * @param {string} severity - Notification severity (low/medium/high)
     * @param {string} icon - Notification icon name
     * @param {string} title - Notification title
     * @param {string} message - Notification message
     * @returns {HTMLElement} Notification element
     */
    function createNotification(severity, icon, title, message) {
        const notificationDiv = document.createElement('div');
        notificationDiv.className = `notification-card notification-${severity} p-3`;
        
        notificationDiv.innerHTML = `
            <div class="d-flex align-items-center">
                <div class="notification-icon">
                    <i class="fas fa-${icon}"></i>
                </div>
                <div>
                    <h5 class="mb-1">${title}</h5>
                    <p class="mb-0 text-muted">${message}</p>
                </div>
            </div>
        `;
        
        return notificationDiv;
    }
});

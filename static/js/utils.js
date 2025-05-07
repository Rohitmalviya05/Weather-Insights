/**
 * Utility functions for the Weather Insights application
 */

// Global constants
const API_ENDPOINT = '/api';

/**
 * Display an error message in a target element
 * @param {string} targetId - ID of the element to show error in
 * @param {string} message - Error message to display
 */
function showError(targetId, message) {
    const target = document.getElementById(targetId);
    if (!target) return;
    
    target.innerHTML = `
        <div class="alert alert-danger">
            <i class="fas fa-exclamation-circle me-2"></i>
            ${message}
        </div>
    `;
}

/**
 * Format a date object to a readable string
 * @param {Date} date - Date object to format
 * @param {Object} options - Formatting options
 * @returns {string} Formatted date string
 */
function formatDate(date, options = {}) {
    const defaultOptions = {
        weekday: 'short',
        month: 'short',
        day: 'numeric'
    };
    
    const formatOptions = { ...defaultOptions, ...options };
    return date.toLocaleDateString('en-US', formatOptions);
}

/**
 * Format time from a Date object
 * @param {Date} date - Date object to extract time from
 * @param {boolean} hour12 - Whether to use 12-hour format
 * @returns {string} Formatted time string
 */
function formatTime(date, hour12 = true) {
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: hour12
    });
}

/**
 * Get current location using Geolocation API
 * @returns {Promise} Promise resolving to coordinates object
 */
function getCurrentLocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('Geolocation is not supported by your browser'));
            return;
        }
        
        navigator.geolocation.getCurrentPosition(
            (position) => {
                resolve({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                });
            },
            (error) => {
                let errorMessage;
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage = 'Location access was denied. Please enable location services.';
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage = 'Location information is unavailable.';
                        break;
                    case error.TIMEOUT:
                        errorMessage = 'The request to get location timed out.';
                        break;
                    default:
                        errorMessage = 'An unknown error occurred while getting location.';
                }
                reject(new Error(errorMessage));
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    });
}

/**
 * Initialize a Leaflet map
 * @param {string} elementId - ID of the element to create map in
 * @param {number} latitude - Initial latitude
 * @param {number} longitude - Initial longitude
 * @param {number} zoom - Initial zoom level
 * @returns {Object} Leaflet map object
 */
function initMap(elementId, latitude = 40.7128, longitude = -74.0060, zoom = 12) {
    const map = L.map(elementId).setView([latitude, longitude], zoom);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);
    
    return map;
}

/**
 * Create a map marker
 * @param {Object} map - Leaflet map object
 * @param {number} latitude - Marker latitude
 * @param {number} longitude - Marker longitude
 * @param {Object} options - Marker options
 * @returns {Object} Leaflet marker object
 */
function createMapMarker(map, latitude, longitude, options = {}) {
    const defaultOptions = {
        draggable: false,
        title: 'Location'
    };
    
    const markerOptions = { ...defaultOptions, ...options };
    return L.marker([latitude, longitude], markerOptions).addTo(map);
}

/**
 * Debounce function to limit the rate at which a function can fire
 * @param {Function} func - Function to debounce
 * @param {number} wait - Milliseconds to wait
 * @returns {Function} Debounced function
 */
function debounce(func, wait = 300) {
    let timeout;
    return function(...args) {
        const context = this;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
}

/**
 * Format temperature with unit
 * @param {number} temp - Temperature value
 * @param {string} unit - Temperature unit ('C' or 'F')
 * @returns {string} Formatted temperature string
 */
function formatTemperature(temp, unit = 'C') {
    if (typeof temp !== 'number') return '--°' + unit;
    return `${Math.round(temp)}°${unit}`;
}

/**
 * Get wind direction as a string based on degrees
 * @param {number} degrees - Wind direction in degrees
 * @returns {string} Wind direction as a string (N, NE, E, etc.)
 */
function getWindDirection(degrees) {
    const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
    const index = Math.round(degrees / 22.5) % 16;
    return directions[index];
}

/**
 * Initialize AOS library
 */
function initAOS() {
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true
        });
    }
}

// Initialize AOS when DOM is loaded
document.addEventListener('DOMContentLoaded', initAOS);

// Export utilities for use in other scripts
window.utils = {
    showError,
    formatDate,
    formatTime,
    getCurrentLocation,
    initMap,
    createMapMarker,
    debounce,
    formatTemperature,
    getWindDirection
};

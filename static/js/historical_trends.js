/**
 * Historical Trends page functionality
 */
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const locationInput = document.getElementById('location-input');
    const searchBtn = document.getElementById('search-btn');
    const trendsContainer = document.getElementById('trends-container');
    const noTrendsContainer = document.getElementById('no-trends-container');
    const addressSuggestions = document.getElementById('address-suggestions');
    
    // Chart objects
    let temperatureChart = null;
    let precipitationChart = null;
    
    // Handle search button click
    searchBtn.addEventListener('click', function() {
        const location = locationInput.value.trim();
        
        if (location) {
            // Show loading state
            searchBtn.disabled = true;
            searchBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';
            
            // Split location into city and country
            const parts = location.split(',').map(part => part.trim());
            let city = parts[0];
            let country = parts.length > 1 ? parts[1] : '';
            
            // Fetch historical trends
            fetchHistoricalTrends(city, country)
                .then(data => {
                    displayHistoricalTrends(data);
                    trendsContainer.style.display = 'block';
                    noTrendsContainer.style.display = 'none';
                })
                .catch(error => {
                    console.error('Error fetching historical trends:', error);
                    alert('Failed to fetch historical trends. Please try again.');
                })
                .finally(() => {
                    searchBtn.disabled = false;
                    searchBtn.innerHTML = 'Analyze Trends';
                });
        } else {
            alert('Please enter a location.');
        }
    });
    
    // Handle location input for autocomplete
    locationInput.addEventListener('input', utils.debounce(function() {
        const query = this.value.trim();
        
        if (query.length < 3) {
            addressSuggestions.style.display = 'none';
            return;
        }
        
        // In a real implementation, you would call a geocoding API here
        // For demo, show some sample suggestions
        showSampleSuggestions(query);
    }, 300));
    
    /**
     * Show sample location suggestions
     * @param {string} query - Search query
     */
    function showSampleSuggestions(query) {
        const sampleLocations = [
            'London, UK',
            'New York, US',
            'Tokyo, JP',
            'Paris, FR',
            'Sydney, AU',
            'Berlin, DE',
            'Toronto, CA'
        ];
        
        const filteredLocations = sampleLocations.filter(location => 
            location.toLowerCase().includes(query.toLowerCase())
        );
        
        if (filteredLocations.length > 0) {
            addressSuggestions.innerHTML = '';
            
            filteredLocations.forEach(location => {
                const item = document.createElement('div');
                item.className = 'address-suggestion-item';
                item.textContent = location;
                
                item.addEventListener('click', function() {
                    locationInput.value = location;
                    addressSuggestions.style.display = 'none';
                });
                
                addressSuggestions.appendChild(item);
            });
            
            addressSuggestions.style.display = 'block';
        } else {
            addressSuggestions.style.display = 'none';
        }
    }
    
    /**
     * Fetch historical trends data
     * @param {string} city - City name
     * @param {string} country - Country name or code
     * @returns {Promise} Promise resolving to historical trends data
     */
    function fetchHistoricalTrends(city, country) {
        // In a real implementation, this would make an API call
        return new Promise(resolve => {
            setTimeout(() => {
                // Sample data for demonstration
                const data = {
                    city: city,
                    country: country,
                    currentMonth: new Date().toLocaleString('default', { month: 'long' }),
                    summary: `${city} is experiencing temperatures slightly above the historical average for this time of year, with precipitation levels below normal.`,
                    tempVsLastYear: '+1.5°C',
                    tempVsAverage: '+0.8°C',
                    precipVsAverage: '-15%',
                    recordHighs: 2,
                    recordLows: 0,
                    temperature: {
                        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                        current: [5, 7, 10, 13, 17, 20, 22, 22, 19, 14, 10, 6],
                        average: [4, 5, 8, 11, 15, 18, 20, 20, 17, 13, 9, 5],
                        min: [0, 1, 3, 6, 10, 13, 15, 15, 12, 8, 4, 1],
                        max: [8, 10, 13, 16, 20, 23, 26, 25, 22, 17, 12, 9]
                    },
                    precipitation: {
                        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                        current: [50, 40, 45, 40, 35, 30, 25, 30, 35, 45, 50, 55],
                        average: [60, 50, 50, 45, 40, 35, 30, 35, 40, 50, 55, 60]
                    }
                };
                
                resolve(data);
            }, 1500);
        });
    }
    
    /**
     * Display historical trends data
     * @param {Object} data - Historical trends data
     */
    function displayHistoricalTrends(data) {
        // Update location title
        document.getElementById('location-title').textContent = `${data.city}, ${data.country} Weather Trends`;
        
        // Update current month
        document.getElementById('current-month').textContent = data.currentMonth;
        
        // Update summary
        document.getElementById('trends-summary').textContent = data.summary;
        
        // Update comparison values
        document.getElementById('temp-vs-last-year').textContent = data.tempVsLastYear;
        document.getElementById('temp-vs-average').textContent = data.tempVsAverage;
        document.getElementById('precip-vs-average').textContent = data.precipVsAverage;
        
        // Update record counts
        document.getElementById('record-highs').textContent = data.recordHighs;
        document.getElementById('record-lows').textContent = data.recordLows;
        
        // Create temperature chart
        createTemperatureChart(data.temperature);
        
        // Create precipitation chart
        createPrecipitationChart(data.precipitation);
    }
    
    /**
     * Create temperature chart
     * @param {Object} data - Temperature data
     */
    function createTemperatureChart(data) {
        const ctx = document.getElementById('temperature-chart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (temperatureChart) {
            temperatureChart.destroy();
        }
        
        // Create new chart
        temperatureChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'This Year',
                        data: data.current,
                        borderColor: '#4361ee',
                        backgroundColor: 'rgba(67, 97, 238, 0.1)',
                        borderWidth: 3,
                        fill: false,
                        tension: 0.4
                    },
                    {
                        label: '10-Year Average',
                        data: data.average,
                        borderColor: '#6c757d',
                        backgroundColor: 'rgba(108, 117, 125, 0.1)',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        fill: false,
                        tension: 0.4
                    },
                    {
                        label: 'Record High',
                        data: data.max,
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231, 76, 60, 0.1)',
                        borderWidth: 1,
                        fill: false,
                        tension: 0.4
                    },
                    {
                        label: 'Record Low',
                        data: data.min,
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        borderWidth: 1,
                        fill: false,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    },
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: 'Temperature (°C)'
                        }
                    }
                }
            }
        });
    }
    
    /**
     * Create precipitation chart
     * @param {Object} data - Precipitation data
     */
    function createPrecipitationChart(data) {
        const ctx = document.getElementById('precipitation-chart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (precipitationChart) {
            precipitationChart.destroy();
        }
        
        // Create new chart
        precipitationChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'This Year',
                        data: data.current,
                        backgroundColor: 'rgba(67, 97, 238, 0.7)',
                        borderColor: '#4361ee',
                        borderWidth: 1
                    },
                    {
                        label: '10-Year Average',
                        data: data.average,
                        backgroundColor: 'rgba(108, 117, 125, 0.4)',
                        borderColor: '#6c757d',
                        borderWidth: 1,
                        type: 'line',
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    },
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: 'Precipitation (mm)'
                        },
                        beginAtZero: true
                    }
                }
            }
        });
    }
});

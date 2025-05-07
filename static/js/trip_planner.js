/**
 * Trip Planner page functionality
 */
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const tripForm = document.getElementById('trip-form');
    const destinationCity = document.getElementById('destination-city');
    const destinationCountry = document.getElementById('destination-country');
    const tripStartDate = document.getElementById('trip-start-date');
    const tripEndDate = document.getElementById('trip-end-date');
    const planTripBtn = document.getElementById('plan-trip-btn');
    const popularDestinations = document.querySelectorAll('.popular-destination');
    const tripRecommendationsContainer = document.getElementById('trip-recommendations-container');
    const noTripContainer = document.getElementById('no-trip-container');
    const printPackingListBtn = document.getElementById('print-packing-list');
    
    // Initialize date pickers
    if (typeof flatpickr !== 'undefined') {
        // Configure start date picker
        const startDatePicker = flatpickr(tripStartDate, {
            minDate: 'today',
            dateFormat: 'Y-m-d',
            onChange: function(selectedDates, dateStr) {
                // Update end date picker min date
                endDatePicker.set('minDate', dateStr);
                
                // If end date is before start date, update it
                if (endDatePicker.selectedDates[0] < selectedDates[0]) {
                    endDatePicker.setDate(selectedDates[0]);
                }
            }
        });
        
        // Configure end date picker
        const endDatePicker = flatpickr(tripEndDate, {
            minDate: 'today',
            dateFormat: 'Y-m-d'
        });
    }
    
    // Handle trip form submission
    tripForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const city = destinationCity.value.trim();
        const country = destinationCountry.value.trim();
        const startDate = tripStartDate.value;
        const endDate = tripEndDate.value;
        
        if (!city || !country || !startDate || !endDate) {
            alert('Please fill out all fields');
            return;
        }
        
        planTripBtn.disabled = true;
        planTripBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Planning...';
        
        // Fetch trip recommendations
        fetchTripRecommendations(city, country, startDate, endDate)
            .then(data => {
                displayTripRecommendations(data);
                tripRecommendationsContainer.style.display = 'block';
                noTripContainer.style.display = 'none';
            })
            .catch(error => {
                console.error('Error fetching trip recommendations:', error);
                alert('Failed to fetch trip recommendations. Please try again.');
            })
            .finally(() => {
                planTripBtn.disabled = false;
                planTripBtn.innerHTML = 'Get Trip Recommendations';
            });
    });
    
    // Handle popular destination clicks
    popularDestinations.forEach(destination => {
        destination.addEventListener('click', function(e) {
            e.preventDefault();
            
            const city = this.dataset.city;
            const country = this.dataset.country;
            
            destinationCity.value = city;
            destinationCountry.value = country;
            
            // Set default dates if not already set
            if (!tripStartDate.value) {
                const tomorrow = new Date();
                tomorrow.setDate(tomorrow.getDate() + 1);
                
                const nextWeek = new Date();
                nextWeek.setDate(nextWeek.getDate() + 8);
                
                if (typeof flatpickr !== 'undefined') {
                    tripStartDate._flatpickr.setDate(tomorrow);
                    tripEndDate._flatpickr.setDate(nextWeek);
                } else {
                    tripStartDate.value = formatDateForInput(tomorrow);
                    tripEndDate.value = formatDateForInput(nextWeek);
                }
            }
            
            // Scroll to form
            tripForm.scrollIntoView({ behavior: 'smooth' });
        });
    });
    
    // Handle print packing list button click
    if (printPackingListBtn) {
        printPackingListBtn.addEventListener('click', function() {
            window.print();
        });
    }
    
    /**
     * Format a date object for input value (YYYY-MM-DD)
     * @param {Date} date - Date object
     * @returns {string} Formatted date string
     */
    function formatDateForInput(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }
    
    /**
     * Fetch trip recommendations data
     * @param {string} city - Destination city
     * @param {string} country - Destination country
     * @param {string} startDate - Trip start date
     * @param {string} endDate - Trip end date
     * @returns {Promise} Promise resolving to trip recommendations data
     */
    function fetchTripRecommendations(city, country, startDate, endDate) {
        // In a real implementation, this would call the API
        return new Promise(resolve => {
            setTimeout(() => {
                // Parse dates
                const start = new Date(startDate);
                const end = new Date(endDate);
                
                // Format date range for display
                const formattedStart = start.toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric'
                });
                
                const formattedEnd = end.toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                });
                
                // Sample trip data
                const tripData = {
                    city: city,
                    country: country,
                    startDate: formattedStart,
                    endDate: formattedEnd,
                    weatherSummary: `Weather for ${city} during your trip is expected to be mostly warm and sunny with occasional cloudy periods. Average temperatures will range from 18°C to 26°C.`,
                    avgTemp: 22,
                    minTemp: 18,
                    maxTemp: 26,
                    essentials: [
                        'Passport & travel documents',
                        'Credit/debit cards',
                        'Local currency',
                        'Phone & charger',
                        'Travel insurance details',
                        'Medications'
                    ],
                    clothing: [
                        'T-shirts & tops',
                        'Shorts',
                        'Light sweater for evenings',
                        'Comfortable walking shoes',
                        'Sandals',
                        'Swimwear',
                        'Sleepwear'
                    ],
                    accessories: [
                        'Sunglasses',
                        'Sunhat',
                        'Day bag / backpack',
                        'Watch',
                        'Camera'
                    ],
                    other: [
                        'Sunscreen (SPF 30+)',
                        'Insect repellent',
                        'Travel adapter',
                        'Reusable water bottle',
                        'Basic first-aid supplies',
                        'Hand sanitizer',
                        'Travel guide / map'
                    ]
                };
                
                resolve(tripData);
            }, 1500);
        });
    }
    
    /**
     * Display trip recommendations
     * @param {Object} data - Trip recommendations data
     */
    function displayTripRecommendations(data) {
        // Update destination title
        document.getElementById('destination-title').textContent = `${data.city}, ${data.country}`;
        
        // Update trip dates
        document.getElementById('trip-dates').textContent = `${data.startDate} - ${data.endDate}`;
        
        // Update weather summary
        document.getElementById('weather-summary').textContent = data.weatherSummary;
        
        // Update temperature info
        document.getElementById('avg-temp').textContent = `${data.avgTemp}°C`;
        document.getElementById('min-temp').textContent = `${data.minTemp}°C`;
        document.getElementById('max-temp').textContent = `${data.maxTemp}°C`;
        
        // Update packing lists
        updatePackingList('essentials-list', data.essentials);
        updatePackingList('clothing-list', data.clothing);
        updatePackingList('accessories-list', data.accessories);
        updatePackingList('other-list', data.other);
    }
    
    /**
     * Update a packing list with items
     * @param {string} listId - ID of the list element
     * @param {Array} items - Array of items to add to the list
     */
    function updatePackingList(listId, items) {
        const listElement = document.getElementById(listId);
        
        if (!listElement) return;
        
        listElement.innerHTML = '';
        
        items.forEach(item => {
            const li = document.createElement('li');
            li.className = 'packing-item';
            
            li.innerHTML = `
                <div class="form-check">
                    <input class="form-check-input packing-checkbox" type="checkbox" id="item-${encodeURIComponent(item.toLowerCase().replace(/\s/g, '-'))}">
                    <label class="form-check-label" for="item-${encodeURIComponent(item.toLowerCase().replace(/\s/g, '-'))}">
                        ${item}
                    </label>
                </div>
            `;
            
            listElement.appendChild(li);
        });
    }
});

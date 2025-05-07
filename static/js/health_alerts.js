// Get health data by coordinates
async function getHealthDataByCoordinates(lat, lon) {
    try {
        showLoading();

        // Get selected conditions
        const selectedConditions = Array.from(document.querySelectorAll('.health-conditions input[type="checkbox"]:checked'))
            .map(checkbox => checkbox.value);

        // Get selected age group
        const ageGroup = document.getElementById('ageGroupSelect').value;

        // Build API URL with parameters
        const params = new URLSearchParams({
            lat: lat,
            lon: lon,
            age_group: ageGroup,
            conditions: selectedConditions.join(',')
        });

        const response = await fetch(`/api/health-alerts?${params}`);
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Failed to fetch health data');
        }

        // Update UI components
        updateHealthAlerts(data.alerts);
        updateCurrentConditions(data.current_weather);
        updateForecastTable(data.daily_forecast);

        // Show success message
        showToastNotification('Health data updated successfully');

    } catch (error) {
        console.error('Error:', error);
        handleApiError(error);
    }
}

function updateHealthAlerts(alerts) {
    const container = document.getElementById('healthAlertsContainer');
    if (!alerts || alerts.length === 0) {
        container.innerHTML = `
            <div class="alert alert-info">
                <i class="fas fa-info-circle me-2"></i>
                No health alerts for current conditions
            </div>
        `;
        return;
    }

    const alertsHtml = alerts.map(alert => `
        <div class="alert alert-warning">
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${alert}
        </div>
    `).join('');

    container.innerHTML = alertsHtml;
}

function updateCurrentConditions(weather) {
    const container = document.getElementById('currentConditions');
    if (!weather) {
        container.innerHTML = '<div class="alert alert-info">Weather data unavailable</div>';
        return;
    }

    container.innerHTML = `
        <div class="d-flex align-items-center mb-3">
            <i class="fas fa-thermometer-half fs-2 me-3"></i>
            <div>
                <h4 class="mb-0">${Math.round(weather.temp)}°C</h4>
                <p class="mb-0">${weather.description}</p>
            </div>
        </div>
        <div class="row">
            <div class="col-6">
                <p><i class="fas fa-tint me-2"></i>Humidity: ${weather.humidity}%</p>
            </div>
        </div>
    `;
}

function updateForecastTable(forecast) {
    const tbody = document.getElementById('forecastTableBody');
    if (!forecast || forecast.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">Forecast data unavailable</td></tr>';
        return;
    }

    tbody.innerHTML = forecast.map(day => `
        <tr>
            <td>${day.day}</td>
            <td>
                <i class="fas fa-thermometer-half me-2"></i>${Math.round(day.temp)}°C
            </td>
            <td><span class="badge bg-info">${day.air_quality_index}</span></td>
            <td><span class="badge bg-warning">${day.pollen_level}</span></td>
            <td><span class="badge bg-danger">${day.uv_index}</span></td>
            <td><span class="badge bg-secondary">${day.health_risk}</span></td>
        </tr>
    `).join('');
}

// Placeholder functions -  These need to be implemented in the actual application
function showLoading() {
    // Implement loading indicator logic here
    console.log("Showing loading indicator");
}

function showToastNotification(message) {
  //Implement toast notification logic here
  console.log("Showing toast notification: ", message);
}


function loadHealthTrends() {
    fetch('/api/health-trends')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update charts
                document.getElementById('tempTrendChart').src = `/static/charts/health/${data.data.charts.temperature}`;
                document.getElementById('humidityChart').src = `/static/charts/health/${data.data.charts.humidity}`;
                
                // Update metrics
                const metrics = data.data.metrics;
                const metricsHtml = `
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h6>Temperature</h6>
                                <p>High Temperature Days: ${metrics.high_temp_days}</p>
                                <p>Low Temperature Days: ${metrics.low_temp_days}</p>
                                <p>Average: ${metrics.avg_temperature.toFixed(1)}°C</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h6>Humidity</h6>
                                <p>High Humidity Days: ${metrics.high_humidity_days}</p>
                                <p>Average: ${metrics.avg_humidity.toFixed(1)}%</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h6>Common Conditions</h6>
                                ${Object.entries(metrics.common_conditions)
                                    .map(([condition, count]) => `<p>${condition}: ${count}</p>`)
                                    .join('')}
                            </div>
                        </div>
                    </div>
                `;
                document.getElementById('healthMetrics').innerHTML = metricsHtml;
            }
        })
        .catch(error => {
            console.error('Error loading health trends:', error);
            document.getElementById('healthTrendsContainer').innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Error loading health trends
                </div>
            `;
        });
}

// Call loadHealthTrends when page loads
document.addEventListener('DOMContentLoaded', loadHealthTrends);

function handleApiError(error) {
  //Implement API error handling logic here
  console.error("API Error:", error);
  //Example: Display an error message to the user.
  alert("An error occurred. Please try again later.");
}
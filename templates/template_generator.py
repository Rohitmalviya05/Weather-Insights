"""
Script to generate placeholder templates for all pages.
This is used to create templates for all required routes so links work.
"""

import os

# List of all template pages needed
TEMPLATES = [
    {
        "filename": "clothing_recommendations.html",
        "title": "Clothing Recommendations",
        "description": "Get AI-powered clothing and outfit recommendations based on the current and forecasted weather."
    },
    {
        "filename": "historical_trends.html",
        "title": "Historical Trends",
        "description": "Analyze weather patterns and historical data to spot trends and make better predictions."
    },
    {
        "filename": "commute_forecast.html",
        "title": "Commute Forecast",
        "description": "Plan your travel with detailed weather forecasts along your commute route."
    },
    {
        "filename": "gardening_weather.html",
        "title": "Gardening Weather",
        "description": "Specialized weather information and tips for gardeners and agricultural activities."
    },
    {
        "filename": "trip_planner.html",
        "title": "Trip Planner",
        "description": "Plan your trips with detailed weather forecasts and packing recommendations."
    },
    {
        "filename": "smart_notifications.html",
        "title": "Smart Notifications",
        "description": "Receive personalized weather alerts and notifications for important weather changes."
    },
    {
        "filename": "custom_widgets.html",
        "title": "Custom Widgets",
        "description": "Create and embed customized weather widgets for your website or application."
    },
    {
        "filename": "map.html",
        "title": "Weather Map",
        "description": "Interactive weather map with real-time conditions and forecast data."
    },
    {
        "filename": "login.html",
        "title": "Login",
        "description": "Log in to your Weather Insights account to access personalized features."
    },
    {
        "filename": "signup.html",
        "title": "Sign Up",
        "description": "Create a new account to access personalized weather information and save your preferences."
    },
    {
        "filename": "profile.html",
        "title": "Profile",
        "description": "Manage your account settings and personalized weather preferences."
    },
    {
        "filename": "feedback.html",
        "title": "Feedback",
        "description": "Share your feedback and suggestions to help us improve."
    },
    {
        "filename": "thank_you.html",
        "title": "Thank You",
        "description": "Thanks for submitting your feedback."
    },
]

# Template content
TEMPLATE_CONTENT = """{% extends 'base.html' %}

{% block title %}{{ title }} - Weather Insights{% endblock %}

{% block content %}
<div class="container mb-5">
    <h1 class="section-heading">{{ title }}</h1>
    <p class="section-subheading">{{ description }}</p>
    
    <div class="row mb-5">
        <div class="col-lg-8">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h3 class="card-title mb-0">{{ title }} Feature</h3>
                </div>
                <div class="card-body p-4">
                    <div class="text-center py-5">
                        <div class="mb-4">
                            <i class="fas {{ icon }} fa-4x text-primary mb-3"></i>
                            <h4>This feature is coming soon!</h4>
                            <p class="text-muted">We're currently working on enhancing this feature. Check back soon for updates!</p>
                        </div>
                        <a href="{{ url_for('main.index') }}" class="btn btn-primary mt-3">
                            <i class="fas fa-home me-2"></i>Back to Home
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-lg-4">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h3 class="card-title mb-0">Related Features</h3>
                </div>
                <div class="card-body">
                    <div class="list-group">
                        <a href="{{ url_for('main.weather') }}" class="list-group-item list-group-item-action">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <i class="fas fa-cloud me-2 text-primary"></i>
                                    Weather Forecast
                                </div>
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </a>
                        <a href="{{ url_for('main.hyper_local') }}" class="list-group-item list-group-item-action">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <i class="fas fa-map-marked-alt me-2 text-primary"></i>
                                    Hyper-Local Forecast
                                </div>
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </a>
                        <a href="{{ url_for('main.map') }}" class="list-group-item list-group-item-action">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <i class="fas fa-map me-2 text-primary"></i>
                                    Weather Map
                                </div>
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

# Icons for each template
ICONS = {
    "clothing_recommendations.html": "fa-tshirt",
    "historical_trends.html": "fa-chart-line",
    "commute_forecast.html": "fa-car",
    "gardening_weather.html": "fa-seedling",
    "trip_planner.html": "fa-suitcase",
    "smart_notifications.html": "fa-bell",
    "custom_widgets.html": "fa-laptop-code",
    "map.html": "fa-map",
    "login.html": "fa-sign-in-alt",
    "signup.html": "fa-user-plus",
    "profile.html": "fa-user-cog",
    "feedback.html": "fa-comment-alt",
    "thank_you.html": "fa-check-circle"
}

def generate_templates():
    """Generate all the template files."""
    for template in TEMPLATES:
        filename = template["filename"]
        title = template["title"]
        description = template["description"]
        icon = ICONS.get(filename, "fa-star")
        
        content = TEMPLATE_CONTENT.replace("{{ title }}", title)
        content = content.replace("{{ description }}", description)
        content = content.replace("{{ icon }}", icon)
        
        with open(f"{filename}", "w") as f:
            f.write(content)
            
        print(f"Created template: {filename}")

if __name__ == "__main__":
    generate_templates()
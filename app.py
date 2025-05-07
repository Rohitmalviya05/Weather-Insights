from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
import os
from datetime import datetime
import logging

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=None):
    """Create and configure the Flask application"""
    load_dotenv()  # Load environment variables from .env file

    app = Flask(__name__)

    # Basic configuration
    app.config["SECRET_KEY"] = os.environ.get("SESSION_SECRET", "dev-key-for-testing")

    # Set DB URI with fallback to local SQLite in instance/
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///instance/weather.db"
    )

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Configure secure headers with ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Set up user loader for Flask-Login
    from models import User, WeatherPreference, LocationFavorite, FeedbackEntry
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user from database for Flask-Login"""
        return User.query.get(int(user_id))
    
    # Redirect to login if user is not authenticated
    login_manager.login_view = "main.login"  # Make sure this route exists

    # Register blueprints
    from routes import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    
    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 errors"""
        return render_template('error.html', 
                              error_code=404, 
                              error_message="Page not found"), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        """Handle 500 errors"""
        return render_template('error.html', 
                              error_code=500,
                              error_message="Internal server error"), 500
    
    # Add template filters
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%Y-%m-%d %H:%M'):
        """Convert a timestamp to formatted date"""
        if isinstance(value, (int, float)):
            value = datetime.fromtimestamp(value)
        return value.strftime(format)
    
    @app.template_filter('timestamp_to_time')
    def timestamp_to_time(value, format='%H:%M'):
        """Convert a timestamp to time format"""
        if isinstance(value, (int, float)):
            value = datetime.fromtimestamp(value)
        return value.strftime(format)
    
    # Add context processors
    @app.context_processor
    def inject_now():
        """Inject current time into templates"""
        return {'now': datetime.now()}

    # Set up logging
    if not app.debug:
        logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Create database tables
    with app.app_context():
        db.create_all()
        logger.info("Database tables created (if they didn't exist)")

    return app


# Create the application instance
app = create_app()

# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

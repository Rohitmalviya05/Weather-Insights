from datetime import datetime
from extensions import db  # Import db from extensions.py
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """User account model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    preferences = relationship("WeatherPreference", back_populates="user", cascade="all, delete-orphan")
    favorite_locations = relationship("LocationFavorite", back_populates="user", cascade="all, delete-orphan")
    feedback_entries = relationship("FeedbackEntry", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# Other models follow the same pattern, using `db` from extensions.py
class WeatherPreference(db.Model):
    """User weather preferences model"""
    __tablename__ = 'weather_preferences'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    temperature_unit = Column(String(1), default='C')  # C for Celsius, F for Fahrenheit
    wind_speed_unit = Column(String(3), default='m/s')  # m/s, km/h, mph
    notification_enabled = Column(Boolean, default=True)
    health_alerts_enabled = Column(Boolean, default=True)
    health_conditions = Column(String(255), default='')  # Comma-separated health conditions

    # Relationships
    user = relationship("User", back_populates="preferences")

    def __repr__(self):
        return f'<WeatherPreference user_id={self.user_id}>'

class LocationFavorite(db.Model):
    """User favorite locations model"""
    __tablename__ = 'location_favorites'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    location_name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="favorite_locations")

    def __repr__(self):
        return f'<LocationFavorite {self.location_name}>'


class FeedbackEntry(db.Model):
    """User feedback model"""
    __tablename__ = 'feedback_entries'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # Can be anonymous
    feedback_type = Column(String(50), nullable=False)  # general, bug, feature
    subject = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)  # 1-5 rating
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="feedback_entries")

    def __repr__(self):
        return f'<Feedback {self.subject}>'


class WeatherLog(db.Model):
    """Weather data log for historical comparisons"""
    __tablename__ = 'weather_logs'

    id = Column(Integer, primary_key=True)
    location_name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    pressure = Column(Integer, nullable=False)
    wind_speed = Column(Float, nullable=False)
    wind_direction = Column(Integer, nullable=False)
    weather_condition = Column(String(50), nullable=False)
    weather_description = Column(String(100), nullable=False)
    uv_index = Column(Float, nullable=True)
    air_quality_index = Column(Integer, nullable=True)
    pollen_level = Column(Integer, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<WeatherLog {self.location_name} at {self.recorded_at}>'


class PageVisit(db.Model):
    """Analytics for page visits"""
    __tablename__ = 'page_visits'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # Can be anonymous
    page_name = Column(String(100), nullable=False)
    visit_time = Column(DateTime, default=datetime.utcnow)
    user_agent = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 support

    def __repr__(self):
        return f'<PageVisit {self.page_name} at {self.visit_time}>'
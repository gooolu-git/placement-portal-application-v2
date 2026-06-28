import os
from datetime import timedelta
from dotenv import load_dotenv

# Automatically load variables from the .env file into os.environ
load_dotenv()

class Config:
    """Configuration class loading environment variables for the Placement Portal V2 backend."""
    
    # 1. Security Keys (JWT & Flask Sessions)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-fallback-secret-key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default-dev-fallback-jwt-key')
    
    # Token expiration time (2 hours for VueJS sessions)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    
    # 2. Database Configuration (SQLite)
    # If DATABASE_URL is not set in .env, it defaults to creating 'placement_portal.db' in the backend root
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

    # 3. Redis Configuration (Required for Caching & Celery)
    # REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')
    
    # Celery Configuration for Batch/Scheduled Jobs
    # CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', REDIS_URL)
    # CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', REDIS_URL)
    
    # 4. Flask-Mail / Notification Configuration (Daily Reminders & Monthly Reports)
    # MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
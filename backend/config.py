import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    
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
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')
    CACHE_DEFAULT_TIMEOUT = 60
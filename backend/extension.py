from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_caching import Cache
from config import Config

db = SQLAlchemy()
jwt = JWTManager()
cache =Cache()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    CORS(app, origins=['http://localhost:5173', 'http://localhost:5000'])
    
    return app
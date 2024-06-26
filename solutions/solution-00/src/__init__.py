from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

load_dotenv()  # Charger les variables d'environnement à partir du fichier .env

cors = CORS()
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app() -> Flask:
    """
    Create a Flask app with the given configuration class.
    The default configuration class is DevelopmentConfig.
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Déterminer l'environnement à partir de la variable d'environnement FLASK_ENV
    env = os.getenv('FLASK_ENV', 'development')

    # Configurer l'application en fonction de l'environnement
    if env == 'production':
        app.config.from_object('config.ProductionConfig')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('PROD_DATABASE_URL')
        app.config['DATABASE_TYPE'] = os.getenv('PROD_DATABASE_TYPE')
    elif env == 'testing':
        app.config.from_object('config.TestingConfig')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')
        app.config['DATABASE_TYPE'] = os.getenv('TEST_DATABASE_TYPE')
    else:
        app.config.from_object('config.DevelopmentConfig')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DEV_DATABASE_URL')
        app.config['DATABASE_TYPE'] = os.getenv('DEV_DATABASE_TYPE')

    register_extensions(app)
    register_routes(app)
    register_handlers(app)

    return app

def register_extensions(app: Flask) -> None:
    """Register the extensions for the Flask app"""
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    with app.app_context():
        db.create_all()
    # Further extensions can be added here

def register_routes(app: Flask) -> None:
    """Import and register the routes for the Flask app"""
    from src.routes.users import users_bp
    from src.routes.countries import countries_bp
    from src.routes.cities import cities_bp
    from src.routes.places import places_bp
    from src.routes.amenities import amenities_bp
    from src.routes.reviews import reviews_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(amenities_bp)

def register_handlers(app: Flask) -> None:
    """Register the error handlers for the Flask app."""
    app.errorhandler(404)(lambda e: (
        {"error": "Not found", "message": str(e)}, 404
    ))
    app.errorhandler(400)(lambda e: (
        {"error": "Bad request", "message": str(e)}, 400
    ))

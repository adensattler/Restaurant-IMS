from flask import Flask
from app.extensions import oauth
from app.auth import init_auth
import app.database as database  # Your custom database module


def create_app():
    """ Application factory: Assembles and returns clones of your app """
    app = Flask(__name__)
    app.config.from_object("config")     # load the current_app.config with the vars from .env 

    # Initialize extensions
    oauth.init_app(app)
    database.init_app(app)  # Initialize custom database

    # Initialize Auth0
    init_auth(app)

    # Register blueprints (if you have any)
    from .base import base as base_blueprint
    app.register_blueprint(base_blueprint)
    

    return app


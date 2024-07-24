from flask import Flask
from .extensions import oauth, scheduler
from .init_functions import init_auth, init_scheduler
from . import database  # My custom database module


def create_app():
    """ Application factory: Assembles and returns clones of your app """
    app = Flask(__name__)
    app.config.from_object("config")     # load the current_app.config with the vars from .env 

    # INITIALIZE EXTENTIONS ------------------------------------------
    oauth.init_app(app)
    database.init_app(app)  # Initialize custom database for Flask

    # Initialize Auth0
    init_auth(app)
    
    # Initialize scheduler
    init_scheduler(app)

    # Register blueprints 
    from .base import base as base_blueprint
    app.register_blueprint(base_blueprint)
    

    return app


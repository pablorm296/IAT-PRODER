from flask import Flask
from datetime import timedelta
import os
import flask

from IAT.Config import Reader
from IAT.Views import Front

def create_app(debug = None):
    # Are we in a debug env
    if os.environ["FLASK_DEBUG_IAT"] == "True" and debug is None:
        debug = True

    # Read configuration
    if debug:
        myConfigReader = Reader(path = "Debug", load = "app")
    else:
        myConfigReader = Reader(path = None, load = "app")

    CONFIG = myConfigReader.Config

    # Create a new app
    app = Flask(__name__, static_folder = "Static", template_folder = "Templates", instance_relative_config = True)

    # Define app key
    if debug:
        app.secret_key = "DEBUG_KEY"
    else:
        app.secret_key = myConfigReader.Config["app"]["secret_key"].encode()
        
    # Register blueprints
    app.register_blueprint(Front)

    # Set session cookie expiration
    @app.before_request
    def make_session_permanent():
        flask.session.permanent = True
        app.permanent_session_lifetime = timedelta(days = 365)

    return app
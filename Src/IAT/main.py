from flask import Flask
from datetime import timedelta
import os
import flask
import logging

from IAT.Config import Reader
from IAT.Views import Front, Api

def create_app(debug = None):
    # Are we in a debug env
    if os.environ["FLASK_DEBUG_IAT"] == "True":
        debug = True
    else:
        debug = False

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
    app.register_blueprint(Api)

    # Register not found error handler
    @app.errorhandler(404)
    def notFoundErrorHandler(e):
        # Render error page
        return flask.render_template("404.html")

    # Set session cookie expiration
    @app.before_request
    def make_session_permanent():
        flask.session.permanent = True
        app.permanent_session_lifetime = timedelta(days = 365)

    # If debug, disable cache (faster debugging)
    if debug:
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    # If debug, set logger debug
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    
    return app
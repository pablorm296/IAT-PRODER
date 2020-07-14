from flask import Flask

def create_app(debug = True):
    # Create a new app
    app = Flask(__name__, static_folder = "/Static", template_folder = "/Templates", instance_relative_config = True)
    # Define app key
    if debug:
        app.secret_key = "DEBUG_KEY"
    else:
        pass
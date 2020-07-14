import flask
from flask import Blueprint

# Define front-end (client-side) blueprint
Front = Blueprint('front', __name__, static_folder = "/Static", template_folder = "/Templates", url_prefix = "/")

@Front.route("/", methods = ["GET"])
def landing():
    """Landing view.

    Although not implemented yet, this view is intended to check user device. If it's a mobile device, user will be redirected to the mobile version of the test. If not, it will be redirected to the desktop version.

    """
    # TODO: Check for mobile devices. For now, only desktop versions
    flask.redirect("welcome", 302)

@Front.route("/welcome", methods = ["GET"])
def welcome():
    pass


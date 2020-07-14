import flask
import uuid
import pymongo
import os
from IAT.Config import Reader
from flask import Blueprint
from flask import session

# Read config
# CHeck if we are in a test env
if os.environ["FLASK_DEBUG_IAT"] == "True":
    ConfigReader = Reader(path = "./Debug", load = "all")
else:
    ConfigReader = Reader(path = None, load = "all")

CONFIG = ConfigReader.Config
MONGO_URI = ConfigReader.Mongo_Uri

# Define front-end (client-side) blueprint
Front = Blueprint('front', __name__, static_folder = "Static", template_folder = "Templates", url_prefix = "/")

@Front.route("/", methods = ["GET"])
def landing():
    """Landing view.

    Although not implemented yet, this view is intended to check user device. If it's a mobile device, user will be redirected to the mobile version of the test. If not, it will be redirected to the desktop version.

    """
    # TODO: Check for mobile devices. For now, only desktop versions
    flask.redirect("welcome", 302)

@Front.route("/welcome", methods = ["GET"])
def welcome():
    # Check if session has user_id field
    if session.get("user_id", None):
        # If not, then create a new user_id
        session["user_id"] = uuid.uuid1().hex
        # Render welcome
        return flask.render_template("welcome.html.jinja")
    # If there is a user_id in the session cookie
    else:
        # Open new DB connection
        MongoConnection = pymongo.MongoClient(MONGO_URI)
        MongoDB = MongoConnection[CONFIG["app"]["mongo_db_name"]]
        UsersCollection = MongoDB[CONFIG["app"]["mongo_users_collections"]]

        # Search user id
        user_id = session.get("user_id")
        searchResults = UsersCollection.find_one(
            {"user_id": user_id}
        )

        # If there is not a registered user, or if the user has not completed the test, then render instructions
        if searchResults is None or searchResults["completed"] == False:
            return flask.render_template("welcome.html.jinja")
        else:
            return flask.render_template("sorry.html.jinja")



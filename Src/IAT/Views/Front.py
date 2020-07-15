import flask
import uuid
import pymongo
import datetime
import logging
import os
import re
from flask import Blueprint
from flask import session
from flask import request

from IAT.Config import Reader

# COnfigure logger
logger = logging.getLogger(__name__)

# Read config
# CHeck if we are in a test env
if os.environ["FLASK_DEBUG_IAT"] == "True":
    ConfigReader = Reader(path = "./Debug", load = "app")
else:
    ConfigReader = Reader(path = None, load = "app")

# Define global config variables
CONFIG = ConfigReader.Config
MONGO_URI = ConfigReader.Mongo_Uri

# Define front-end (client-side) blueprint
Front = Blueprint('front', __name__, static_folder = "Static", template_folder = "Templates", url_prefix = "/")

@Front.route("/", methods = ["GET"])
def landing():
    """Landing View.

    Although not implemented yet, this view is intended to check user device. If it's a mobile device, user will be redirected to the mobile version of the test. If not, it will be redirected to the desktop version.

    """
    # TODO: Check for mobile devices. For now, only desktop versions
    return flask.redirect("welcome", 302)

@Front.route("/welcome", methods = ["GET"])
def welcome():
    """Welcome View

    When a `GET` request is received, this view will get the `user_id` from the session cookie and check if the user has already completed the test. If the user has already completed the test, a message will be rendered stating that he or she can only participate in one test. However, if the user is new or has not completed a test, the main welcome message will be rendered.

    """
    # Check if session has user_id field
    if session.get("user_id", None) is None:
        # If not, then create a new user_id
        session["user_id"] = uuid.uuid1().hex
        # Register user in database
        # Open new DB connection
        MongoConnection = pymongo.MongoClient(MONGO_URI)
        MongoDB = MongoConnection[CONFIG["app"]["mongo_db_name"]]
        UsersCollection = MongoDB[CONFIG["app"]["mongo_users_collection"]]

        # insert new user id
        user_id = session.get("user_id")
        insertResults = UsersCollection.insert_one(
            {
                "user_id": user_id,
                "created": datetime.datetime.utcnow(),
                "remote_address": request.remote_addr,
                "last_seen": datetime.datetime.utcnow(),
                "hits": 1,
                "completed": False
            }
        )

        # Check insert result
        if not insertResults.acknowledged:
            error_msg = "Something went wrong when creating a new user. "
            logger.error(error_msg)
            raise Exception(error_msg)
        
        # Close mongo connection
        MongoConnection.close()
        
        # Render welcome
        return flask.render_template("welcome.html")

    # If there is a user_id in the session cookie
    else:
        # Open new DB connection
        MongoConnection = pymongo.MongoClient(MONGO_URI)
        MongoDB = MongoConnection[CONFIG["app"]["mongo_db_name"]]
        UsersCollection = MongoDB[CONFIG["app"]["mongo_users_collection"]]

        # Search user id
        user_id = session.get("user_id")
        searchResults = UsersCollection.find_one(
            {"user_id": user_id}
        )

        # If there is not a registered user, or if the user has not completed the test, then render main welcome message
        if searchResults is None or searchResults["completed"] == False:
            # Try to update user access info
            updateResults = UsersCollection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "last_seen": datetime.datetime.utcnow()
                    },
                    "$inc": {
                        "hits": 1
                    }
                }
            )

            # Close connection
            MongoConnection.close()

            return flask.render_template("welcome.html")
        else:
            return flask.render_template("sorry.html")

@Front.route("/instructions", methods = ["GET"])
def instructions():
    # Check referer
    referer = request.headers.get("Referer", None)
    # If there's not a referer header, go to root
    if referer is None:
        logger.warning("Request from {0} attempted to directly access instructions without referer".format(request.remote_addr))
        return flask.redirect("/", 302)
    
    # Check referer
    matchResult = re.findall(r"\/welcome", referer)
    if len(matchResult) < 1:
        logger.warning("Request from {0} attempted to directly access instructions with an invalid referer ('{1}')".format(request.remote_addr, referer))
        return flask.redirect("/", 302)


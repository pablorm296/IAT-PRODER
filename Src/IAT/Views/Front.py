import flask
import uuid
import datetime
import logging
import os
import re
import random
import json
import pandas as pd
from flask import Blueprint, session, request

# Imports from package
from IAT.Config import Reader
from IAT.Common.DB import MongoConnector, DBShortcuts
from IAT.Common.Exceptions import FrontEndException

# Configure logger
logger = logging.getLogger(__name__)

# Read config
# Check if we are in a test env
if os.environ["FLASK_DEBUG_IAT"] == "True":
    ConfigReader = Reader(path = "./Debug", load = "all")
else:
    ConfigReader = Reader(path = None, load = "all")

# Define global config variables
CONFIG = ConfigReader.Config
MONGO_URI = ConfigReader.Mongo_Uri
STIMULI_WORDS = CONFIG["stimuli"]["words"]
STIMULI_IMAGES = CONFIG["stimuli"]["images"]
MONGO_DB = CONFIG["app"]["mongo_db_name"]
MONGO_USERS_COLLECTION = CONFIG["app"]["mongo_users_collection"]
MONGO_RESULTS_COLLECTION = CONFIG["app"]["mongo_results_collection"] 
MONGO_COUNTER_COLLECTION = CONFIG["app"]["mongo_counter_collection"]

# Define front-end (client-side) blueprint
Front = Blueprint('front', __name__, static_folder = "Static", template_folder = "Templates", url_prefix = "/")

# Function that checks the user referer
def checkReferer(referer: str, requestHeaders):
    # Check referer
    requestReferer = request.headers.get("Referer", None)
    # If there's not a referer header, go to root
    if requestReferer is None:
        logger.warning("Request from {0} attempted to directly access instructions without referer".format(request.remote_addr))
        return False
    
    # Check referer
    matchResult = re.findall(r"\/{0}".format(referer), requestReferer)
    if len(matchResult) < 1:
        logger.warning("Request from {0} attempted to directly access instructions with an invalid referer ('{1}')".format(request.remote_addr, requestReferer))
        return False

    # If we arrived up to this point, return True
    return True

# Function that checks session info
def checkSession(session):
    # Check user id in session cookie
    if session.get("user_id", None) is None:
        logger.warning("Request from {0} attempted to directly access IAT without session cookie".format(request.remote_addr))
        return False
    
    # If we arrived up to this point, return True 
    return True

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
        MongoConnection = MongoConnector(MONGO_DB, MONGO_USERS_COLLECTION, MONGO_URI)

        # insert new user id
        user_id = session.get("user_id")
        insertResults = MongoConnection.collection.insert_one(
            {
                "user_id": user_id,
                "created": datetime.datetime.utcnow(),
                "remote_address": request.remote_addr,
                "last_seen": datetime.datetime.utcnow(),
                "hits": 1,
                "completed": False,
                "last_view": "welcome"
            }
        )

        # Check insert result
        if not insertResults.acknowledged:
            error_msg = "Something went wrong while registering a new user in the database. The insert operation was not acknowledged."
            logger.error(error_msg)
            raise FrontEndException(error_msg)
        
        # Close mongo connection
        MongoConnection.close()
        
        # Render welcome
        return flask.render_template("welcome.html")

    # If there is a user_id in the session cookie
    else:
        # Open new DB connection
        MongoConnection = MongoConnector(MONGO_DB, MONGO_USERS_COLLECTION, MONGO_URI)

        # Search user id
        user_id = session.get("user_id")
        searchResults = MongoConnection.collection.find_one(
            {"user_id": user_id}
        )

        # Close connection
        MongoConnection.close()
                
        # if the user has not completed the test, then render main welcome message
        if searchResults["completed"] == False or searchResults is None:
            # Try to update user access info
            DBShortcuts.updateLastUserView("welcome", searchResults["user_id"])

            # Render welcome page
            return flask.render_template("welcome.html")
        else:
            # Render message saying that the user already answered the test
            return flask.render_template("sorry.html")

@Front.route("/instructions", methods = ["GET"])
def instructions():
    """Instructions View

    When a `GET` request is received, this view will display some general instructions and examples for the IAT.

    If the request contains an invalid referer or session cookie, the user will be redirected to the root (`/`) of the application.

    """
    
    # Check referer and session
    if not checkReferer("welcome", request.headers) or not checkSession(session):
        return flask.redirect("/", 302)
    
    # Get user_id
    user_id = session.get("user_id")

    # Try to update user access info
    updated = DBShortcuts.updateLastUserView("instructions", user_id)
    
    # Check if the user was successfully updated
    if not updated:
        error_msg = "Something went wrong while registering the user action. The database couldn't update the document."
        logger.error(error_msg)
        raise FrontEndException(error_msg)

    # Render instructions template
    # We're going to randomly shuffle each word and image list
    response_env = {
        "good_words": random.sample(list(filter(lambda d: d['label'] in ['good'], STIMULI_WORDS)), k = 8),
        "bad_words": random.sample(list(filter(lambda d: d['label'] in ['bad'], STIMULI_WORDS)), k = 8),
        "white_people": random.sample(list(filter(lambda d: d['label'] in ['white'], STIMULI_IMAGES)), k = 4),
        "dark_people": random.sample(list(filter(lambda d: d['label'] in ['dark'], STIMULI_IMAGES)), k = 4)
    }
    return flask.render_template("instructions.html", **response_env)

@Front.route("/iat", methods = ["GET"])
def iat():

    # Check referer and session
    if not checkReferer("instructions", request.headers) or not checkSession(session):
        return flask.redirect("/", 302)

    # Get user_id
    user_id = session.get("user_id")
    
    # Try to update user access info
    updated = DBShortcuts.updateLastUserView("iat", user_id)

    # Check if the user was successfully updated
    if not updated:
        error_msg = "Something went wrong while registering the user action. The database couldn't update the document."
        logger.error(error_msg)
        raise FrontEndException(error_msg)

    # Render main iat template
    return flask.render_template("iat.html")

@Front.route("/survey", methods = ["GET"])
def survey():

    # Check referer and session
    if not checkReferer("iat", request.headers) or not checkSession(session):
        return flask.redirect("/", 302)

    # Get user_id
    user_id = session.get("user_id")
    
    # Try to update user access info
    updated = DBShortcuts.updateLastUserView("survey", user_id)

    # Check if the user was successfully updated
    if not updated:
        error_msg = "Something went wrong while registering the user action. The database couldn't update the document."
        logger.error(error_msg)
        raise FrontEndException(error_msg)

    # Render survey template
    return flask.render_template("survey.html")

@Front.route("/results", methods = ["GET"])
def results():

    # Check referer and session
    if not checkReferer("survey", request.headers) or not checkSession(session):
        return flask.redirect("/", 302)
    
    # Get user_id
    user_id = session.get("user_id")
    
    # Try to update user access info
    updated = DBShortcuts.updateLastUserView("survey", user_id)

    # Check if the user was successfully updated
    if not updated:
        error_msg = "Something went wrong while registering the user action. The database couldn't update the document."
        logger.error(error_msg)
        raise FrontEndException(error_msg)

    # Read user results
    MongoConnection = MongoConnector(MONGO_DB, MONGO_RESULTS_COLLECTION, MONGO_URI)
    readResults = MongoConnection.collection.find_one(
        {"user_id": user_id}
    )

    # Check if there's at least one user with results
    if readResults is None:
        logger.warning("Request from {0} attempted to render results, but user is not registered in results database".format(request.remote_addr))
        return flask.redirect("/", 302)

    # Load results
    userResults = readResults["results"]
    userOrder = readResults["order"]

    # Close connection
    MongoConnection.close()

    # Define response dict in advance
    responseEnv = dict()

    # Check number of results
    MongoConnection = MongoConnector(MONGO_DB, MONGO_COUNTER_COLLECTION, MONGO_URI)
    readResults = MongoConnection.collection.find_one(
        {"counter_name": "n_results"}
    )

    # Check if mongo did find the document containing the number of results
    if readResults is None:
        error_msg = "Something went wrong while looking for the results counter."
        logger.error(error_msg)
        raise FrontEndException(error_msg)

    # Check number of results
    # If we still have less than 41 results, then we use Harvard's results
    if readResults["counter_value"] < 41:
        # Open json file with Harvard results
        try:
            with open("Data/d_scores.json") as jsonFile:
                dScores = json.load(jsonFile)
        except Exception:
            error_msg = "Something went wrong while loading other users' results."
            logger.error(error_msg)
            raise FrontEndException(error_msg)
    # Else, just load our own dScores
    else:
        dScores = readResults["scoresArray"]

    # Get round latency results. Depending on user order (1 or 0, randomly assigned), we flip round results order
    # If round is 0
    if userOrder == 0:
        roundResults_3 = userResults.get("round_3", None)
        roundResults_4 = userResults.get("round_4", None)
        roundResults_6 = userResults.get("round_6", None)
        roundResults_7 = userResults.get("round_7", None)
    # If round is 1
    elif userOrder == 1:
        roundResults_3 = userResults.get("round_6", None)
        roundResults_4 = userResults.get("round_7", None)
        roundResults_6 = userResults.get("round_3", None)
        roundResults_7 = userResults.get("round_4", None)

    # Coerce each round result into a dataFrame (pandas library)
    roundResults_3_df = pd.DataFrame(roundResults_3)
    roundResults_4_df = pd.DataFrame(roundResults_4)
    roundResults_6_df = pd.DataFrame(roundResults_6)
    roundResults_7_df = pd.DataFrame(roundResults_7)
    # Create a list containing the dataframes
    roundResults_list = list()
    roundResults_list.append(roundResults_3_df)
    roundResults_list.append(roundResults_4_df)
    roundResults_list.append(roundResults_6_df)
    roundResults_list.append(roundResults_7_df)
    
    # Remove answers where latency > 10 000 ms
    for stageNum in range(0, 4):
        df_foo = roundResults_list[stageNum]
        df_foo = df_foo[df_foo["latency"] < 10000]
        roundResults_list[stageNum] = df_foo

    # Create a dataframe with the pooled latencies from rounds 3, 4, 6, and 7
    roundResults_pooled = pd.concat([roundResults_3_df, roundResults_4_df, roundResults_6_df, roundResults_7_df], ignore_index = True)

    # Count the total number of trials in the pooled dataframe
    # We can't just use the total number of trials, because we removed some of them (the ones with latency > 10 000 ms)
    nRow = len(roundResults_pooled.index)

    # Check that no more than 10% of the pooled latency results were under 300 ms
    nRow_lessThan300 = roundResults_pooled[roundResults_pooled["latency"] < 300].shape[0]
    if (nRow_lessThan300 / nRow) > 0.1 :
        # If more than 10% of the results, send error code e.1 (Results were random and we can't analyze them)
        resultData = {"code": "e.1"}
        responseEnv = {
            "resultData": json.dumps(resultData)
        }
        return flask.render_template("results.html", **responseEnv)

    # For each stage, compute latency mean.
    stageMeans = dict()
    for stageNum in range(0, 4):
        stageDataFrame = roundResults_list[stageNum]
        # Only consider trials where user made 0 mistakes
        stageDataFrame = stageDataFrame[stageDataFrame["error"] == 0]
        stageLatencies = stageDataFrame["latency"]
        latencyMean = stageLatencies.mean()
        stageMeans["stage_{0}".format(stageNum)] = latencyMean

    # Now, consider only trials where user made a mistake. In those cases, replace latency with stage mean + 600
    for stageNum in range(0, 4):
        stageDataFrame = roundResults_list[stageNum]
        latencyMean = stageMeans["stage_{0}".format(stageNum)]
        # Replace trials where errors > 0 with the stage mean
        stageDataFrame.loc[stageDataFrame["error"] > 0] = latencyMean + 600
        roundResults_list[stageNum] = stageDataFrame

    # For each stage, compute the "new mean" (considering the cases where latency was replaced with mean+600)
    newStageMeans = dict()
    for stageNum in range(0, 4):
        stageDataFrame = roundResults_list[stageNum]
        stageLatencies = df_foo["latency"]
        latencyMean = stageLatencies.mean()
        newStageMeans["stage_{0}".format(stageNum)] = latencyMean

    # Compute standard deviations
    # One standard deviations for stage group 1 (stages 3 and 6)
    # One standard deviations for stage group 2 (stages 4 and 7)
    SD1 = pd.concat([roundResults_list[0]["latency"], roundResults_list[2]["latency"]], ignore_index = True).std()
    SD2 = pd.concat([roundResults_list[1]["latency"], roundResults_list[3]["latency"]], ignore_index = True).std()

    # Compute "IAT effect"
    Q1 = (newStageMeans["stage_0"] - newStageMeans["stage_2"]) / SD1
    Q2 = (newStageMeans["stage_1"] - newStageMeans["stage_3"]) / SD2

    IAT = (Q1 + Q2) / 2 # This is why our "IAT effect" can only range from -2 to 2!!

    # Add IAT effect (dScore) to array of dScores
    MongoConnection = MongoConnector(MONGO_DB, MONGO_COUNTER_COLLECTION, MONGO_URI)
    updateResults = MongoConnection.collection.update_one(
        {"counter_name": "n_results"},
        {
            "$inc": {
                "counter_value": 1
            },
            "$push": {
                "scoresArray": IAT
            }
        }
    )

    # Check update operation
    if updateResults.modified_count < 1:
        error_msg = "Something went wrong while updating the results array."
        logger.error(error_msg)
        raise FrontEndException(error_msg)

    # Get fastest latency
    fastestLatency = roundResults_pooled["latency"].min()

    # Get slowest latency
    slowestLatency = roundResults_pooled["latency"].max()

    # Get mean pooled latency
    meanLatency = roundResults_pooled["latency"].mean()

    # Get total number of errors
    totalErrors = roundResults_pooled["error"].sum()

    # Coerce data types
    fastestLatency = int(fastestLatency)
    slowestLatency = int(slowestLatency)
    meanLatency = float(meanLatency)
    totalErrors = int(totalErrors)
    # Round to 4 decimal places
    meanLatency = round(meanLatency, 3)
    IAT = round(IAT, 3)

    # Prepare results data
    resultData = {"code": "s", "iatScore": IAT, "fastestLatency": fastestLatency,
    "slowestLatency": slowestLatency, "meanLatency": meanLatency, "errorCount": totalErrors,
    "dScores": dScores}

    # Put data in response env
    responseEnv = {
        "resultData": json.dumps(resultData)
    }

    # Render
    return flask.render_template("results.html", **responseEnv)

@Front.route("/bye", methods = ["GET"])
def bye():

    # Check referer and session
    if not checkReferer("results", request.headers) or not checkSession(session):
        return flask.redirect("/", 302)

    return flask.render_template("bye.html")
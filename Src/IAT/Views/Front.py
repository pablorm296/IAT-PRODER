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

# Package imports
from IAT.Config import Reader
from IAT.Common.DB import MongoConnector, DBShortcuts
from IAT.Common.Exceptions import FrontEndException

# Configure logger
logger = logging.getLogger(__name__)

# Read config
# Check if we are in a test env
if os.environ["FLASK_DEBUG_IAT"] == "True":
    DEBUG_MODE = True
    ConfigReader = Reader(path = "./Debug", load = "all")
else:
    DEBUG_MODE = False
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
RECAPTCHA_PUBLIC = CONFIG["app"]["google_reCaptcha_public"]
RECAPTCHA_PRIVATE = CONFIG["app"]["google_reCaptcha_private"]

# Define front-end (client-side) blueprint
Front = Blueprint('front', __name__, static_folder = "Static", static_url_path = "/Static", template_folder = "Templates", url_prefix = "/")

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

    return flask.redirect("welcome", 302)

@Front.route("/welcome", methods = ["GET"])
def welcome():

    # First, check if we're dealing with a mobile-device user
    mobileUserRegex = r"Mobile|iP(hone|od|ad)|Android|BlackBerry|IEMobile|Kindle|NetFront|Silk-Accelerated|(hpw|web)OS|Fennec|Minimo|Opera M(obi|ini)|Blazer|Dolfin|Dolphin|Skyfire|Zune"
    userAgent = request.headers.get("User-Agent", None)

    # If no user agent or empty
    if userAgent is None or userAgent == "":
        raise FrontEndException("Although a valid HTTP request was received, the User-Agent header is missing!")

    # Check if user agent matches mobile
    mobileUserAgentMatch = re.search(mobileUserRegex, userAgent)

    # If match failed, then user is not mobile
    if mobileUserAgentMatch is not None:
        # Set mobile parameter in session accordingly
        session["mobile"] = True
    else:
        session["mobile"] = False

    # Check if session has user_id field
    if session.get("user_id", None) is None:
        
        # Register user
        DBShortcuts.registerNewUser(session, request)
        
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
                
        # If we can't find that userid, then we register it int he database
        if searchResults is None:
            
            # Register user
            DBShortcuts.registerNewUser(session, request)

            # Render welcome page
            return flask.render_template("welcome.html")

        # if the user has not completed the test, then render main welcome message
        elif searchResults["completed"] == False:
            # Close connection
            MongoConnection.close()
            # Try to update user access info
            DBShortcuts.updateLastUserView("welcome", searchResults["user_id"])
            # Render welcome page
            return flask.render_template("welcome.html")

        elif searchResults["completed"]:
            # Close connection
            MongoConnection.close()

            if DEBUG_MODE:
                return flask.render_template("welcome.html")
            else:
                # Render message saying that the user already answered the test
                return flask.render_template("sorry.html")

@Front.route("/instructions", methods = ["GET"])
def instructions():
    
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
    response_env = {
        "reCaptcha_public": RECAPTCHA_PUBLIC
    }
    return flask.render_template("survey.html", **response_env)

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

    # Set completed status to true
    MongoConnection = MongoConnector(MONGO_DB, MONGO_USERS_COLLECTION, MONGO_URI)
    updateResults = MongoConnection.collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "completed": True
            }
        }
    )

    if updateResults.modified_count < 1:
        error_msg = "Something went wrong while setting the 'completed' status. The database couldn't update the document."
        logger.error(error_msg)
        raise FrontEndException(error_msg)

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
        dScores = readResults["scores_array"]

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
        stageLatencies = stageDataFrame["latency"]
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

    # First, check if the user is not registered in the array of scores
    MongoConnection = MongoConnector(MONGO_DB, MONGO_COUNTER_COLLECTION, MONGO_URI)

    searchResults = MongoConnection.collection.count_documents({
        "scores_array.user_id": user_id
    })

    if searchResults < 1:
        # Add IAT effect (dScore) to array of dScores
        updateResults = MongoConnection.collection.update_one(
            {"counter_name": "n_results"},
            {
                "$inc": {
                    "counter_value": 1
                },
                "$push": {
                    # This is an array where we store user id, together with his/her score
                    "scores_array": {
                        "user_id": user_id,
                        "score": IAT
                    }
                }
            }
        )

        # Check update operation
        if updateResults.modified_count < 1:
            error_msg = "Something went wrong while updating the results array."
            logger.error(error_msg)
            raise FrontEndException(error_msg)

    else:
        logger.warning("User {0} from {1} tried to re submit survey answers.".format(user_id, request.remote_addr))

    # Close DB connection
    MongoConnection.close()

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

    # Check debug mode
    if DEBUG_MODE:
        response_env = {
            "reCaptcha_public": RECAPTCHA_PUBLIC
        }
        return flask.render_template("debug_survey.html", **response_env)
    else:
        return flask.render_template("bye.html")

@Front.route("/errorTest", methods = ["GET"])
def testError():
    error_msg = "User requested a test error page. Everything is fine :)"
    logger.error(error_msg)
    raise FrontEndException(error_msg)

@Front.route("/errorCustom", methods = ["GET"])
def customError():

    # Check message
    msg = request.args.get("msg", None)
    if msg is None or msg == "":
        error_msg = "User requested a custom error page without message"
        logger.error(error_msg)
        raise FrontEndException()
    
    error_msg = "User requested a custom error page with message: {0}".format(msg)
    logger.error(error_msg)
    raise FrontEndException(msg)

@Front.errorhandler(FrontEndException)
@Front.errorhandler(500)
def serverErrorHandler(e):
    # Define response env
    responseEnv = {
        "errorMsg": str(e)
    }
    # Render error page
    return flask.render_template("error.html", **responseEnv), 500

@Front.errorhandler(404)
def notFoundErrorHandler(e):
    # Render error page
    return flask.render_template("404.html"), 404

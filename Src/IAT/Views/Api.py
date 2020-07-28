import flask
import uuid
import pymongo
import datetime
import logging
import os
import re
import random
import requests
import base64

from flask import Blueprint
from flask import session
from flask import request

# Package imports
from IAT.Config import Reader
from IAT.RestfulTools import Response as ApiResponse
from IAT.Common.Exceptions import ApiException, BadRequest
from IAT.Common.DB import MongoConnector, DBShortcuts

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
RECAPTCHA_PUBLIC = CONFIG["app"]["google_reCaptcha_public"]
RECAPTCHA_PRIVATE = CONFIG["app"]["google_reCaptcha_private"]

# Define API blueprint
Api = Blueprint('api', __name__, static_folder = "Static", template_folder = "Templates", url_prefix = "/api")

@Api.route("/", methods = ["GET"])
def hello_world():
    newResponse = ApiResponse("Hello World! (This means that the API is up and running)")
    return newResponse.response

@Api.route("/iat/stimuli", methods = ["GET"])
def getStimuli():
    # Get test stage
    stage = flask.request.args.get('stage', None)

    # If there's not an stage, send error
    if stage is None:
        raise BadRequest("Well... if you don't tell me your stage, how am I supposed to send back some stimuli?")
    
    # Check if stage can be coerced into a integer
    try:
        stage = int(stage)
    except:
        raise BadRequest("Mmm... I'm starting to suspect that you don't know what you're supposed to send")

    # Define data
    if stage == 1:
        # Choose random images
        imageList = random.choices(STIMULI_IMAGES, k = 16)
        finalList = imageList

    elif stage == 2:
        # Choose random words
        wordList = random.choices(STIMULI_WORDS, k = 16)
        finalList = wordList
        
    elif stage >= 3 and stage < 5:
        # Choose training words
        trainWords = random.sample(STIMULI_WORDS, 4)
        # Choose random words
        wordList = random.choices(STIMULI_WORDS, k = 18)
        # Choose random images
        imageList = random.choices(STIMULI_IMAGES, k = 18)
        # Create an empty list
        mergedList = [None] * ( len(wordList) + len(imageList) )
        # Fill every other element with a word
        mergedList[::2] = wordList
        # Fill every other element with an image
        mergedList[1::2] = imageList
        # Concatenate train words with merged list
        finalList = trainWords + mergedList

    elif stage == 5:
        # Choose random images
        imageList = random.choices(STIMULI_IMAGES, k = 16)
        finalList = imageList

    elif stage >= 6 and stage < 8:
        # Choose training words
        trainWords = random.sample(STIMULI_WORDS, 4)
        # Choose random words
        wordList = random.choices(STIMULI_WORDS, k = 18)
        # Choose random images
        imageList = random.choices(STIMULI_IMAGES, k = 18)
        # Create an empty list
        mergedList = [None] * ( len(wordList) + len(imageList) )
        # Fill every other element with a word
        mergedList[::2] = wordList
        # Fill every other element with an image
        mergedList[1::2] = imageList
        # Concatenate train words with merged list
        finalList = trainWords + mergedList
    else:
        raise BadRequest("Well... I don't know what are you expecting me to send in that stage!")

    # Define response data
    responseData = {"stimuli": finalList}
    # Send response
    newResponse = ApiResponse(responseData)
    return newResponse.response

@Api.route("/iat/results", methods = ["POST"])
def postIatResults():
    # Try to get json content
    jsonPayload = flask.request.get_json()
    if jsonPayload is None:
        raise BadRequest("It seems that you're sending me some unexpected data format!")

    # Check json payload content
    if jsonPayload.get("results", None) is None or jsonPayload.get("order", None) is None:
        raise BadRequest("That is an invalid json payload!")

    # Check session
    if session.get("user_id", None) is None:
        raise ApiException("There is not a valid session cookie in this request!")

    # Try to update user access info
    user_id = session.get("user_id")
    DBShortcuts.updateLastUserView("iat_final", user_id)

    # Try to insert user results
    MongoConnection = MongoConnector(MONGO_DB, MONGO_RESULTS_COLLECTION, MONGO_URI)
    insertResults = MongoConnection.collection.insert_one(
        {
            "user_id": user_id,
            "results_inserted": datetime.datetime.utcnow(),
            "results": jsonPayload.get("results"),
            "order": jsonPayload.get("order")
        }
    )
    # Check insert operations
    if not insertResults.acknowledged:
        raise ApiException("Something went wrong while updating the user info or inserting his/her results!")

    # Close pymongo connection
    MongoConnection.close()

    # Send Response
    newResponse = ApiResponse("Ok!")
    return newResponse.response

@Api.route("/survey", methods = ["POST"])
def postSurvey():
    # Try to get json content
    jsonPayload = flask.request.get_json()
    if jsonPayload is None:
        raise BadRequest("It seems that you're sending me some unexpected data format!")

    # Check session
    if session.get("user_id", None) is None:
        raise ApiException("There is not a valid session cookie in this request!")

    # Before anything, let's check the Captcha
    # Get captcha response
    googleCapthca = jsonPayload.get("g", None)
    if googleCapthca is None or googleCapthca == "":
        raise ApiException("Well, if you don't send a valid reCaptcha, I'll think you're a robot!")

    # Ask Google if we have a valid captcha
    logger.info("Validating captcha with Google service...")
    response = requests.post("https://www.google.com/recaptcha/api/siteverify?secret={0}&response={1}".format(RECAPTCHA_PRIVATE, googleCapthca))

    # Parse response as JSON
    try:
        responseAsJson = response.json()
    except Exception:
        raise ApiException("This is embarrasing. I could not ask Google if you're indeed a human!")
    
    # Is the user a human?
    human = responseAsJson.get("success", None)

    if human is None or not human:
        raise ApiException("Get out of here, you filthy robot!")

    newResponse = ApiResponse("Ok!")
    return newResponse.response 

@Api.errorhandler(ApiException)
def ApiErrorHanlder(e):
    errorResponse = ApiResponse({}, e.status_code, True, str(e))
    return errorResponse.response

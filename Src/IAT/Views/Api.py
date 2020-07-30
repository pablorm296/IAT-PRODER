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
import csv

from flask import Blueprint
from flask import session
from flask import request

# Package imports
from IAT.Config import Reader
from IAT.RestfulTools import Response as ApiResponse
from IAT.Common.Exceptions import ApiException, BadRequest, Forbidden, Unauthorized
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
MONGO_SURVEY_COLLECTION = CONFIG["app"]["mongo_survey_collection"]
RECAPTCHA_PUBLIC = CONFIG["app"]["google_reCaptcha_public"]
RECAPTCHA_PRIVATE = CONFIG["app"]["google_reCaptcha_private"]
ADMIN_USER = CONFIG["app"]["admin_user"]
ADMIN_PASSWORD = CONFIG["app"]["admin_password"]

# Define API blueprint
Api = Blueprint('api', __name__, static_folder = "Static", template_folder = "Templates", url_prefix = "/api")

# Function that parses a basic authorization header
def parseBasicAuthorization(authHeader:str):
    # First, split using space
    split = authHeader.split(" ")

    # Check if first part
    if split[0].lower() != "basic":
        raise BadRequest("Unexpected authorization type")

    # Decode second part
    credentials = base64.b64decode(split[1]).decode('utf-8')
    
    # Split decoded credentials
    credentials = credentials.split(":")

    if len(credentials) != 2:
        raise BadRequest("Unexpected credentials format")

    # Return credentials
    return credentials

@Api.route("/", methods = ["GET"])
def hello_world():
    newResponse = ApiResponse("Hello World! (This means that the API is up and running)")
    return newResponse.response

@Api.route("/results/<collection>", methods = ["GET"])
def getResults(collection = None):

    # Check authorization
    AuthHeader = request.headers.get("Authorization", None)

    # If there's not an authorization header
    if AuthHeader is None:
        raise Unauthorized("There's not a valid authorization header")

    # Parse authorization
    credentials = parseBasicAuthorization(AuthHeader)

    # Check user and password
    if credentials[0] != ADMIN_USER or credentials[1] != ADMIN_PASSWORD:
        raise Forbidden("Wrong user and/or password")

    # Check collection parameter
    if collection not in ["users", "survey", "iat", "iatScores"] or collection is None:
        raise BadRequest("Please, enter the name of a valid DB collection.")

    # Random file name
    fileName = uuid.uuid1().hex

    # Define target collection as an empty list. 
    targetCollection = []

    if collection == "users":
        # Open Connection
        MongoConnection = MongoConnector(MONGO_DB, MONGO_USERS_COLLECTION, MONGO_URI)
        # Get users
        targetCollection = MongoConnection.collection.find()

    elif collection == "survey":
        # Open Connection
        MongoConnection = MongoConnector(MONGO_DB, MONGO_SURVEY_COLLECTION, MONGO_URI)
        # Get survey results
        targetCollection = MongoConnection.collection.find()

    elif collection == "iat":
        # Open Connection
        MongoConnection = MongoConnector(MONGO_DB, MONGO_RESULTS_COLLECTION, MONGO_URI)
        # Get iat results
        tmpCollection = MongoConnection.collection.find()

        # Loop through each user results
        for userResults in tmpCollection:
            # Get basic info: id, timestamp, and order
            userIdentifier = {
                "user_id": userResults["user_id"],
                "timestamp": userResults["timestamp"],
                "order": userResults["order"]
            }

            # Now, loop through rounds
            for roundNumber in range(1, 8):
                # Get round key
                testRound = userResults["results"]["round_{0}".format(roundNumber)]
                # Loop through each stimuli
                for stimulus in testRound:
                    # Combine basic user info with stimuli info
                    stimulusInfo = dict(**userIdentifier)
                    stimulusInfo["latency"] = stimulus["latency"]
                    stimulusInfo["type"] = stimulus["img"]
                    stimulusInfo["label"] = stimulus["label"]
                    stimulusInfo["value"] = stimulus["value"]
                    stimulusInfo["error"] = stimulus["error"]
                    stimulusInfo["latency"] = stimulus["latency"]
                    stimulusInfo["round"] = roundNumber
                    # Add to collection
                    targetCollection.append(targetCollection)

    elif collection == "iatScores":
        pass

    # Write document
    with open("Tmp/{0}.csv".format(fileName)) as csvFile:
        # Get fieldnames from first item. This is not very fail proof, since the first element can be "incomplete"
        # To prevent errors, a DB drop must be executed before running this app commit
        fieldNames = list(targetCollection[0].keys())

        # Init file writer (see https://docs.python.org/3/library/csv.html#csv.DictWriter)
        writer = csv.DictWriter(csvFile, fieldNames, "", "ignore")

        # Write file header
        writer.writeheader()

        # Loop through elements in targetCollection (attention: in some cases is a list, in others a cursor)
        for document in targetCollection:
            writer.writerow(document)
    
    # Send file
    return flask.send_file("Tmp/{0}.csv".format(fileName))

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
            "timestamp": datetime.datetime.utcnow(),
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
        logger.warning("Captcha validation failed. Empty captcha response")
        raise ApiException("Well, if you don't send a valid reCaptcha, I'll think you're a robot!")

    # Ask Google if we have a valid captcha
    logger.info("Validating captcha with Google service...")
    response = requests.post("https://www.google.com/recaptcha/api/siteverify?secret={0}&response={1}".format(RECAPTCHA_PRIVATE, googleCapthca))

    # Parse response as JSON
    try:
        responseAsJson = response.json()
    except Exception:
        logger.warning("Captcha validation failed. Received an invalid response format from Google")
        raise ApiException("This is embarrasing. I could not ask Google if you're indeed a human!")
    
    # Is the user a human?
    human = responseAsJson.get("success", None)

    if human is None or not human:
        logger.warning("Captcha validation failed. Google didn't acknowledged the captcha value")
        raise ApiException("Get out of here, you filthy robot!")

    # Clean request payload
    for key in jsonPayload:
        if jsonPayload[key] == "" or jsonPayload[key] == "NONE":
            jsonPayload[key] = None

    # Get user id
    user_id = session.get("user_id")

    # Open DB connection
    MongoConnection = MongoConnector(MONGO_DB, MONGO_SURVEY_COLLECTION, MONGO_URI)

    # Check if user_id is already registered in survey
    searchResults = MongoConnection.collection.count_documents({
        "user_id": user_id
    })

    if searchResults > 0:
        # Log warning
        logger.warning("User {0} from {1} tried to re submit survey answers.".format(user_id, request.remote_addr))
        
        # Return API
        newResponse = ApiResponse("User already answered the survey! POST payload will be ignored.")
        return newResponse.response 

    # Insert user survey responses
    insertResults = MongoConnection.collection.insert_one({
        "user_id": user_id,
        "timestamp": datetime.datetime.utcnow(),
        "age": jsonPayload["srvy_age"],
        "gender": jsonPayload["srvy_sex"],
        "employment": jsonPayload["srvy_lab"],
        "education": jsonPayload["srvy_esc"],
        "nationality": jsonPayload["srvy_country"],
        "state": jsonPayload["srvy_state"],
        "zip": jsonPayload["srvy_zip"],
        "ethnicity": jsonPayload["srvy_eth"],
        "skin": jsonPayload["srvy_skin"],
        "iat": jsonPayload["srvy_iat"],
        "hand": jsonPayload["srvy_hand"],
        "table_q1": jsonPayload["srvy_table_quest_1"],
        "table_q2": jsonPayload["srvy_table_quest_2"],
        "table_q3": jsonPayload["srvy_table_quest_3"],
        "table_q4": jsonPayload["srvy_table_quest_4"]     
    })

    # Close connection
    MongoConnection.close()

    # Check insert
    if not insertResults.acknowledged:
        raise ApiException("Something went while updating the Survey table!")

    newResponse = ApiResponse("Ok!")
    return newResponse.response 

# Define error handler for ApiException class
@Api.errorhandler(ApiException)
def ApiErrorHandler(e):
    errorResponse = ApiResponse({}, e.status_code, True, str(e))
    return errorResponse.response

# Define error handler for general server error
@Api.errorhandler(ApiException)
def InternalServerErrorHandler(e):
    errorResponse = ApiResponse({}, 500, True, str(e))
    return errorResponse.response

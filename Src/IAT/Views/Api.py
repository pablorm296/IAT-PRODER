import flask
import uuid
import pymongo
import datetime
import logging
import os
import re
import random
from flask import Blueprint
from flask import session
from flask import request

from IAT.Config import Reader
from IAT.RestfulTools import Response as ApiResponse
from IAT.Common import ApiException, BadRequest

# Configure logger
logger = logging.getLogger(__name__)

# Read config
# CHeck if we are in a test env
if os.environ["FLASK_DEBUG_IAT"] == "True":
    ConfigReader = Reader(path = "./Debug", load = "all")
else:
    ConfigReader = Reader(path = None, load = "all")

# Define global config variables
CONFIG = ConfigReader.Config
MONGO_URI = ConfigReader.Mongo_Uri
STIMULI_WORDS = CONFIG["stimuli"]["words"]
STIMULI_IMAGES = CONFIG["stimuli"]["images"]

# Define API blueprint
Api = Blueprint('api', __name__, static_folder = "Static", template_folder = "Templates", url_prefix = "/api")

@Api.route("/", methods = ["GET"])
def hello_world():
    newResponse = ApiResponse("Hello World! (This means that the API is up and running)")
    return newResponse.response

@Api.route("/stimuli", methods = ["GET"])
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
        raise BadRequest("Well... I'm not prepared to handle an 8 stages IAT!")

    # Define response data
    responseData = {"stimuli": finalList}
    # Send response
    newResponse = ApiResponse(responseData)
    return newResponse.response

@Api.errorhandler(ApiException)
def ApiErrorHanlder(e):
    errorResponse = ApiResponse({}, e.status_code, True, str(e))
    return errorResponse.response

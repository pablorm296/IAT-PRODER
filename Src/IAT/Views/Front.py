import flask
import uuid
import pymongo
import datetime
import logging
import os
import re
import random
import json
import pandas as pd
from flask import Blueprint
from flask import session
from flask import request

from IAT.Config import Reader

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
                "completed": False,
                "last_view": "welcome"
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
        
        # if the user has not completed the test, then render main welcome message
        if searchResults["completed"] == False or searchResults is None:
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
    """Instructions View

    When a `GET` request is received, this view will display some general instructions and examples for the IAT.

    If the request contains an invalid referer or session cookie, the user will be redirected to the root (`/`) of the application.

    """
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

    # Check session
    if session.get("user_id", None) is None:
        logger.warning("Request from {0} attempted to directly access instructions without session cookie".format(request.remote_addr))
        return flask.redirect("/", 302)

    # Update user view
    # Open new DB connection
    MongoConnection = pymongo.MongoClient(MONGO_URI)
    MongoDB = MongoConnection[CONFIG["app"]["mongo_db_name"]]
    UsersCollection = MongoDB[CONFIG["app"]["mongo_users_collection"]]

    # Update user
    user_id = session.get("user_id")
    # Try to update user access info
    updateResults = UsersCollection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "last_seen": datetime.datetime.utcnow(),
                "last_view": "instructions"
            }
        }
    )

    # Close connection
    MongoConnection.close()

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
    # Check referer
    referer = request.headers.get("Referer", None)
    # If there's not a referer header, go to root
    if referer is None:
        logger.warning("Request from {0} attempted to directly access IAT without referer".format(request.remote_addr))
        return flask.redirect("/", 302)
    
    # Check referer
    matchResult = re.findall(r"\/instructions", referer)
    if len(matchResult) < 1:
        logger.warning("Request from {0} attempted to directly access IAT with an invalid referer ('{1}')".format(request.remote_addr, referer))
        return flask.redirect("/", 302)

    # Check session
    if session.get("user_id", None) is None:
        logger.warning("Request from {0} attempted to directly access IAT without session cookie".format(request.remote_addr))
        return flask.redirect("/", 302)
    
    # Update user view
    # Open new DB connection
    MongoConnection = pymongo.MongoClient(MONGO_URI)
    MongoDB = MongoConnection[CONFIG["app"]["mongo_db_name"]]
    UsersCollection = MongoDB[CONFIG["app"]["mongo_users_collection"]]

    # Update user
    user_id = session.get("user_id")
    # Try to update user access info
    updateResults = UsersCollection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "last_seen": datetime.datetime.utcnow(),
                "last_view": "iat"
            }
        }
    )

    # Close connection
    MongoConnection.close()

    # Render main iat template
    return flask.render_template("iat.html")

@Front.route("/survey", methods = ["GET"])
def survey():
    # Check referer
    referer = request.headers.get("Referer", None)
    # If there's not a referer header, go to root
    if referer is None:
        logger.warning("Request from {0} attempted to directly access survey without referer".format(request.remote_addr))
        return flask.redirect("/", 302)
    
    # Check referer
    matchResult = re.findall(r"\/iat", referer)
    if len(matchResult) < 1:
        logger.warning("Request from {0} attempted to directly access survey with an invalid referer ('{1}')".format(request.remote_addr, referer))
        return flask.redirect("/", 302)

    # Check session
    if session.get("user_id", None) is None:
        logger.warning("Request from {0} attempted to directly access survey without session cookie".format(request.remote_addr))
        return flask.redirect("/", 302)
    
    # Update user view
    # Open new DB connection
    MongoConnection = pymongo.MongoClient(MONGO_URI)
    MongoDB = MongoConnection[CONFIG["app"]["mongo_db_name"]]
    UsersCollection = MongoDB[CONFIG["app"]["mongo_users_collection"]]

    # Update user
    user_id = session.get("user_id")
    # Try to update user access info
    updateResults = UsersCollection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "last_seen": datetime.datetime.utcnow(),
                "last_view": "survey"
            }
        }
    )

    # Close connection
    MongoConnection.close()

    # Render survey template
    return flask.render_template("survey.html")

@Front.route("/results", methods = ["GET"])
def results():
    # Check referer
    referer = request.headers.get("Referer", None)
    # If there's not a referer header, go to root
    if referer is None:
        logger.warning("Request from {0} attempted to directly access results without referer".format(request.remote_addr))
        return flask.redirect("/", 302)
    
    # Check referer
    matchResult = re.findall(r"\/survey", referer)
    if len(matchResult) < 1:
        logger.warning("Request from {0} attempted to directly access results with an invalid referer ('{1}')".format(request.remote_addr, referer))
        return flask.redirect("/", 302)

    # Check session
    if session.get("user_id", None) is None:
        logger.warning("Request from {0} attempted to directly access results without session cookie".format(request.remote_addr))
        return flask.redirect("/", 302)
    
    # Update user view
    # Open new DB connection
    MongoConnection = pymongo.MongoClient(MONGO_URI)
    MongoDB = MongoConnection[CONFIG["app"]["mongo_db_name"]]
    UsersCollection = MongoDB[CONFIG["app"]["mongo_users_collection"]]
    ResultsCollection = MongoDB[CONFIG["app"]["mongo_results_collection"]]

    # Update user
    user_id = session.get("user_id")

    # Try to update user access info
    updateResults = UsersCollection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "last_seen": datetime.datetime.utcnow(),
                "last_view": "results",
                "completed": True
            }
        }
    )

    # Read user results
    readResults = ResultsCollection.find_one(
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

    # Define response dict in avance
    responseEnv = dict()

    # Abrimos el json con los resultados de las demás personas
    with open("Data/d_scores.json") as jsonFile:
        dScores = json.load(jsonFile)

    # Obtenemos los resultados de las rondas 3, 4, 6 y 7
    # Dependiendo del orden en el que le tocó al usuario
    # Personas de piel clara = bueno
    if userOrder == 0:
        roundResults_3 = userResults.get("round_3", None)
        roundResults_4 = userResults.get("round_4", None)
        roundResults_6 = userResults.get("round_6", None)
        roundResults_7 = userResults.get("round_7", None)
    # Personas de piel oscura = bueno
    elif userOrder == 1:
        roundResults_3 = userResults.get("round_6", None)
        roundResults_4 = userResults.get("round_7", None)
        roundResults_6 = userResults.get("round_3", None)
        roundResults_7 = userResults.get("round_4", None)

    # Los convertirmos en pandas data framae
    roundResults_3_df = pd.DataFrame(roundResults_3)
    roundResults_4_df = pd.DataFrame(roundResults_4)
    roundResults_6_df = pd.DataFrame(roundResults_6)
    roundResults_7_df = pd.DataFrame(roundResults_7)
    # Creamos una lista con todos los data frame
    roundResults_list = list()
    roundResults_list.append(roundResults_3_df)
    roundResults_list.append(roundResults_4_df)
    roundResults_list.append(roundResults_6_df)
    roundResults_list.append(roundResults_7_df)
    
    # Eliminamos las respuestas que hayan tardado más de 10'000 milisegundos
    for stageNum in range(0, 4):
        df_foo = roundResults_list[stageNum]
        df_foo = df_foo[df_foo["latency"] < 10000]
        roundResults_list[stageNum] = df_foo

    # Creamos un df con todos los data frame
    roundResults_pooled = pd.concat([roundResults_3_df, roundResults_4_df, roundResults_6_df, roundResults_7_df], ignore_index = True)

    # Creamos una variable para guardar el número total de trials
    nRow = len(roundResults_pooled.index)

    # Verificar que no más del 10% de los casos hayan sido muy rápidos (menos de 300 ms)
    nRow_foo = roundResults_pooled[roundResults_pooled["latency"] < 300].shape[0]
    if (nRow_foo / nRow) > 0.1 :
        resultData = {"code": "e.1"}
        responseEnv = {
            "resultData": json.dumps(resultData)
        }
        return flask.render_template("results.html", **responseEnv)

    # Por cada bloque, calculamos la media
    meanBloques = dict()
    for stageNum in range(0, 4):
        df_foo = roundResults_list[stageNum]
        df_foo = df_foo[df_foo["error"] == 0]
        latency_foo = df_foo["latency"]
        mean = latency_foo.mean()
        meanBloques["bloque_{0}".format(stageNum)] = mean

    # Para los bloques que tienen error, remplazamos por media + 600
    for stageNum in range(0, 4):
        df_foo = roundResults_list[stageNum]
        mean = meanBloques["bloque_{0}".format(stageNum)]
        df_foo.loc[df_foo["error"] > 0] = mean + 600
        roundResults_list[stageNum] = df_foo

    # Por cada bloque, calculamos la media
    newMeanBloques = dict()
    for stageNum in range(0, 4):
        df_foo = roundResults_list[stageNum]
        latency_foo = df_foo["latency"]
        mean = latency_foo.mean()
        newMeanBloques["bloque_{0}".format(stageNum)] = mean

    # Calculamos la desviación estandar (3 y 6; 4 y 7)
    SD1 = pd.concat([roundResults_list[0]["latency"], roundResults_list[2]["latency"]], ignore_index = True).std()
    SD2 = pd.concat([roundResults_list[1]["latency"], roundResults_list[3]["latency"]], ignore_index = True).std()

    # Calculamos el efecto IAT
    Q1 = (newMeanBloques["bloque_0"] - newMeanBloques["bloque_2"]) / SD1
    Q2 = (newMeanBloques["bloque_1"] - newMeanBloques["bloque_3"]) / SD2

    IAT = (Q1 + Q2) / 2

    # Obtenemos respuesta más rápida
    fastestLatency = roundResults_pooled["latency"].min()

    # Obtenemos respuesta más lenta
    slowesttLatency = roundResults_pooled["latency"].max()

    # Obtenemos respuesta media
    meanLatency = roundResults_pooled["latency"].mean()

    # Obtenemos número de errores
    totalErrors = roundResults_pooled["error"].sum()

    # Convertimos en tipos que entiende python
    fastestLatency = int(fastestLatency)
    slowestLatency = int(slowesttLatency)
    meanLatency = float(meanLatency)
    totalErrors = int(totalErrors)
    # Redondeamos a 4 decimales
    meanLatency = round(meanLatency, 3)
    IAT = round(IAT, 3)

    resultData = {"code": "s", "iatScore": IAT, "fastestLatency": fastestLatency,
    "slowestLatency": slowestLatency, "meanLatency": meanLatency, "errorCount": totalErrors,
    "dScores": dScores}

    responseEnv = {
        "resultData": json.dumps(resultData)
    }

    return flask.render_template("results.html", **responseEnv)

@Front.route("/bye", methods = ["GET"])
def bye():
    return flask.render_template("bye.html")
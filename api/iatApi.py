import flask
from flask_classy import FlaskView, route
import json
import subprocess
import requests
import base64
import datetime
import uuid
import random
import pymongo
import pandas as pd

#Flask CORS Solution
from flask_cors import CORS
#Custom packages
from restful.restfulResources import Restful, ErrorHandlers # pylint: disable=import-error

class DBconnection(object):
    def __init__(self, db, collection):
        # Verificamos argumentos proporcionados por el usuario
        if not isinstance(db, str) or not isinstance(collection, str):
            raise ValueError("db and collection must be a str object")

        # Abrimos nuevo cliente de pymongo
        self.client = pymongo.MongoClient()

        # Abrimos conexión a db y colección especificada por el usuario
        self.db = self.client[db]
        self.collection = self.db[collection]

    def __enter__(self):
        return self.collection

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.client.close() 

class API:
    class Users(FlaskView):
        # Función para registrar un nuevo usuario
        @route('new', methods = ['POST'])
        def new(self):
            # Leer cookie de la sesión
            sessionId = flask.request.cookies.get("appSession", None)

            # Si la cookie existe
            if sessionId is not None:
                #Verificar que no haya un usuario registrado con un cuestionario contestado
                with DBconnection("iat_proder", "completed") as db:
                    if db.find_one({"id": sessionId}) is not None:
                        raise Restful.Errors.Generic(409, "Can't participate more than once in a day!")

            # Generar uuid para identificar al usuario
            newId = uuid.uuid4()

            # Convertir uuid en string
            newId_str = str(newId)

            # Obtener ip del visitante
            clientIp = flask.request.headers.get("X-Forwarded-For", None)

            # Obtener fecha y hora de registro
            timeStamp = datetime.datetime.now()
            # Representación en str de la fecha y hora del registro
            timeStamp_str = timeStamp.strftime("%Y-%m-%d, %H:%M:%S")

            # Objeto de usuario
            newUser = {"id": newId_str, "created": timeStamp_str, "registeredAddres": clientIp}

            # Registrar usuario en la base de datos
            with DBconnection("iat_proder", "visitors") as db:
                db.insert_one(newUser)

            # Responder con el nuevo usuario
            response = Restful.Response(responseContent = {"id": newId_str, "created": timeStamp_str})
            return response.jsonify()

    class IAT(FlaskView):
        # Función para obtener un registro aleatorio de estímulos (dependiendo de la étapa del iat)
        @route('stimuli', methods = ['GET'])
        def getStimuli(self):
            # Obtenemos etapa de la prueba
            stage = flask.request.args.get('stage', None)

            # Si no enviaron etapa mandar error
            if stage is None:
                raise Restful.Errors.BadRequest("There are missing parameters in the request!")
            
            # Si sí hay stage, intentar convertilo en un número entero
            try:
                stage = int(stage)
            except:
                raise Restful.Errors.BadRequest("Invalid parameter type!")

            # Cargamos diccionario de estímulos
            with open("/var/www/pabloreyes/IAT/api/data/stimuli.json", encoding = 'utf-8') as stimuliFile:
                stimuli = json.load(stimuliFile)

            # Objeto con imágenes
            stimuli_images = stimuli.get("images")
            # Objeto con palábras
            stimuli_words = stimuli.get("words")

            # Dependiendo de la etapa
            if stage == 1:
                wordList = random.sample(stimuli_words, 16)
                finalList = wordList

            elif stage == 2:
                imageList = random.sample(stimuli_images, 16)
                finalList = imageList

            elif stage >= 3 and stage < 5:
                trainWords = random.sample(stimuli_words, 4)
                wordList = random.sample(stimuli_words, 16)
                imageList = random.sample(stimuli_images, 16)
                mergedList = [None] * ( len(wordList) + len(imageList) )
                mergedList[::2] = wordList
                mergedList[1::2] = imageList
                finalList = trainWords + mergedList

            elif stage == 5:
                wordList = random.sample(stimuli_words, 16)
                finalList = wordList

            elif stage >= 6:
                trainWords = random.sample(stimuli_words, 4)
                wordList = random.sample(stimuli_words, 16)
                imageList = random.sample(stimuli_images, 16)
                mergedList = [None] * ( len(wordList) + len(imageList) )
                mergedList[::2] = wordList
                mergedList[1::2] = imageList
                finalList = trainWords + mergedList

            responseContent = finalList
            response = Restful.Response(responseContent = responseContent)
            return response.jsonify()

        # Función para obtener los resultados del IAT
        @route('result/iat', methods = ['GET'])
        def getIatResults(self):
            # Leer cookie de la sesión
            sessionId = flask.request.cookies.get("appSession", None)

            # Si la cookie no existe
            if sessionId is None:
                raise Restful.Errors.BadRequest("There are missing cookies in the request!")

            # Obtenemos el usuario desde la base
            with DBconnection("iat_proder", "users") as db:
                userDoc = db.find_one({"id": sessionId})
                if userDoc is None:
                    raise Restful.Errors.BadRequest("There are not users registred with that id!") 

            # Verificamos que el usuario tenga un campo de resultados
            userResults = userDoc.get("results", None)
            # Si el usuario no tiene campo de resultados
            if userResults is None:
                raise Restful.Errors.BadRequest("The user has not any registered results!")

             # Verificamos que el usuario tenga un campo de orden
            userOrder = userDoc.get("order", None)
            # Si el usuario no tiene campo de orden
            if userOrder is None:
                raise Restful.Errors.BadRequest("The user has not any registered results!")

            responseContent = dict()

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

            # Verificar que no más del 10% de las filas tengan 10%
            nRow_foo = roundResults_pooled[roundResults_pooled["latency"] < 300].shape[0]
            if (nRow_foo / nRow) > 0.1 :
                responseContent = {"code": "e.1"}
                response = Restful.Response(responseContent = responseContent)
                return response.jsonify()

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

            responseContent = {"code": "s", "iatScore": IAT, "fastestLatency": fastestLatency,
            "slowestLatency": slowestLatency, "meanLatency": meanLatency, "totalErrors": totalErrors}

            response = Restful.Response(responseContent = responseContent)
            response = response.jsonify()
            # Desabilitamos el cache
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return response

        # Función para registrar los resultados del iat
        @route('result/<page>', methods = ['POST'])
        def postResults(self, page):

            # Verificar que el mimeType sea json
            if not flask.request.is_json:
                raise Restful.Errors.BadRequest("Invalid request mimeType!")
            # Obtener el json de la request
            requestContent = flask.request.get_json(force = False, silent = True)
            # Si no se pudo obtener un json
            if requestContent is None:
                raise Restful.Errors.BadRequest("Invalid request body!")

            # Leer cookie de la sesión
            sessionId = flask.request.cookies.get("appSession", None)

            # Si la cookie no existe
            if sessionId is None:
                raise Restful.Errors.BadRequest("There are missing cookies in the request!")

            if page == "iat":
                
                # Obtenemos la lista de los resultados
                results = requestContent.get("results")
                # Obtenemos el orden que le tocó al usuario
                order = requestContent.get("order")

                # Guardamos los resultados
                with DBconnection("iat_proder", "users") as db:
                    db.update_one({
                        "id": sessionId
                    },
                    {
                        "$set": {
                            "results": results,
                            "order": order
                        }
                    })

                # Regresamos resultado
                response = Restful.Response(responseContent = results)
                return response.jsonify()

            elif page == "consent":

                # Obtenemos el consentimiento del usuario
                consentResult = requestContent.get("consent", None)

                # Buscamos la id entre los visitantes, si no está, mandar error
                with DBconnection("iat_proder", "visitors") as db:
                    userDoc = db.find_one({"id": sessionId})
                    if userDoc is None:
                        raise Restful.Errors.BadRequest("There are not users registred with that id!") 

                # Agregamos al visitante a la lista de usuarios y guardamos lo que eligió en el consentimiento
                with DBconnection("iat_proder", "users") as db:
                    # Borramos id para evitar conflictos
                    del userDoc["_id"]
                    # Guaramos consentimiento
                    userDoc["consent"] = consentResult
                    db.insert_one(userDoc) 

                # Regresamos resultado
                del userDoc["_id"]
                response = Restful.Response(responseContent = userDoc)
                return response.jsonify()
            

#Configuramos flask
app = flask.Flask(__name__)
CORS(app)

#Definimos un punto para errores del servidor
@app.errorhandler(500)
def internalServerError(e):
    error = Restful.Errors.InternalServerError("Well... that's embarrasing. An unexpected error was encountered in the server.")
    response = error.jsonify()
    response.status_code = error.statusCode
    return response


# Registrar errores
app.register_error_handler(Restful.Errors.BadRequest, ErrorHandlers.Generic)
app.register_error_handler(Restful.Errors.Unauthorized, ErrorHandlers.Generic)
app.register_error_handler(Restful.Errors.Generic, ErrorHandlers.Generic)

#Registrar clases de la API
API.Users.register(app, route_base = "/versions/1/users")
API.IAT.register(app, route_base = "/versions/1/iat")

#Configuramos __name__ == __main__
if __name__ == '__main__':
    app.run(host = '0.0.0.0', ssl_context = ('/etc/letsencrypt/live/pabloreyes.com.mx/fullchain.pem', '/etc/letsencrypt/live/pabloreyes.com.mx/privkey.pem'))
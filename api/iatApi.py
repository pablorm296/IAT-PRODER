import flask
from flask_classy import FlaskView, route
import json
import subprocess
import requests
import base64
import datetime
import uuid
import random
#Flask CORS Solution
from flask_cors import CORS
#Custom packages
from restful.restfulResources import Restful, ErrorHandlers # pylint: disable=import-error

class API:
    class Users(FlaskView):
        # Función para registrar un nuevo usuario
        @route('new', methods = ['POST'])
        def new(self):
            # Leer cookie de la sesión
            sessionId = flask.request.cookies.get("appSession")

            # Si la cookie existe
            if sessionId is not None:
                #Verificar que no haya un usuario registrado con un cuestionario contestado
                pass

            # Generar uuid para identificar al usuario
            newId = uuid.uuid4()
            # Generar uuid para identificar la sesión
            newSession = uuid.uuid4()

            # Convertir uuid en string
            newId_str = str(newId)
            newSession_str = str(newSession)

            # Obtener ip del visitante
            clientIp = flask.request.remote_addr

            # Obtener fecha y hora de registro
            timeStamp = datetime.datetime.now()
            # Representación en str de la fecha y hora del registro
            timeStamp_str = timeStamp.strftime("%Y-%m-%d, %H:%M:%S")

            # Registrar usuario en la base de datos 

            # Responder con el nuevo usuario
            responseContent = {"id": newId_str, "created": timeStamp_str, "registeredAddres": clientIp}
            response = Restful.Response(responseContent = responseContent)
            return response.jsonify()

    class IAT(FlaskView):
        # Función para obtener un registro aleatorio de estímulos (dependiendo de la étapa del iat)
        @route('stimuli', methods = ['GET'])
        def getStimuli(self):
            # Obtenemos etapa de la prueba
            stage = flask.request.args.get('stage')
            stage = int(stage)

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

        # Función para registrar los resultados del iat
        @route('results', methods = ['POST'])
        def postResults(self):
            pass

#Configuramos flask
app = flask.Flask(__name__)
CORS(app)

#Definimos un punto para errores del servidor
@app.errorhandler(500)
def internalServerError(e):
    raise Restful.Errors.InternalServerError("Well... that's embarrasing. An unexpected error was encountered in the server.")


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
import flask
from flask_classy import FlaskView, route
import json
import subprocess
import requests
import base64
import datetime
import uuid
#Flask CORS Solution
from flask_cors import CORS
#Custom packages
from restful import Restful # pylint: disable-msg=E0611

class API:
    class Users(FlaskView):
        # Función para registrar un nuevo usuario
        @route('new', methods = ['GET'])
        def new(self):
            # Leer cookie de la sesión
            sessionId = flask.request.cookies.get("appSession")

            # Si la cookie existe
            if sessionId is not None:
                #Verificar que no haya un usuario registrado en la base de datos
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
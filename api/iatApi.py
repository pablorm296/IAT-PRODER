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
from restful.restfulResources import Restful, ErrorHandlers # pylint: disable=import-error

class API:
    class Users(FlaskView):
        # Función para registrar un nuevo usuario
        @route('new', methods = ['POST'])
        def new(self):
            # Leer cuerpo de la petición
            requestContent = flask.request.get_json(silent = True, force = True)

            # Si el contenido es None
            if requestContent is None:
                raise Restful.Errors.BadRequest("Invalid request body!")

            # Obtener origen de la request
            requestOrigin = requestContent.get("X_VALIDATOR", "")
            requestOriginDec = base64.b64decode(requestOrigin)
            requestOriginTxt = requestOriginDec.decode('UTF-8')

            # Verificamos origen de la request
            if requestOriginTxt != "FRT0Zx5s0O":
                raise Restful.Errors.BadRequest("Invalid request body! (We're watching you...)")

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

#Configuramos __name__ == __main__
if __name__ == '__main__':
    app.run(host = '0.0.0.0', ssl_context = ('/etc/letsencrypt/live/pabloreyes.com.mx/fullchain.pem', '/etc/letsencrypt/live/pabloreyes.com.mx/privkey.pem'))
import flask

#Este módulo contiene la clase Restful, la cual contiene un conjunto de clases y métodos que hacen más fácil la respuesta del servidor

class Restful():

    class Response():
        def __init__(self, statusCode = 200, statusMessage = "Ok", responseContent = None):
            #Verificamos argumentos proporcionados por el usuario
            statusCode = int(statusCode)
            if type(statusMessage) is not str:
                raise TypeError("statusMessage tiene que ser una string")

            self.statusCode = statusCode
            self.content = {}
            self.content["statusCode"] = statusCode
            self.content["statusMessage"] = statusMessage
            self.content["responseContent"] = responseContent
        
        def updateContent(self, content):
            self.content.update(responseContent = content)

        def updateStatus(self, statusCode, statusMessage):
            #Verificamos argumentos proporcionados por el usuario
            if type(statusMessage) is not str:
                raise TypeError("message tiene que ser una string")
            
            self.statusCode = statusCode
            self.content.update(statusCode = statusCode)
            self.content.update(statusMessage = statusMessage)

        def jsonify(self):
            return flask.jsonify(self.content)

        def dump(self):
            return self.content

    class Errors():

        class Generic(Exception):
            def __init__(self, statusCode, statusMessage):
                Exception.__init__(self)
                self.statusCode = int(statusCode)
                self.statusMessage = statusMessage
                self.response = Restful.Response(self.statusCode, self.statusMessage)

            def jsonify(self):
                return self.response.jsonify()

        class InternalServerError(Exception):
            def __init__(self, statusMessage = "Well... that's embarrasing. An unexpected error was encountered in the server."):
                Exception.__init__(self)
                self.statusCode = 500
                self.statusMessage = statusMessage
                self.response = Restful.Response(self.statusCode, self.statusMessage)

            def jsonify(self):
                return self.response.jsonify()

        class BadRequest(Exception):
            def __init__(self, statusMessage = "Bad Request"):
                Exception.__init__(self)
                self.statusCode = 400
                self.statusMessage = statusMessage
                self.response = Restful.Response(self.statusCode, self.statusMessage)

            def jsonify(self):
                return self.response.jsonify()

        class Unauthorized(Exception):
            def __init__(self, statusMessage = "Unauthorized"):
                Exception.__init__(self)
                self.statusCode = 401
                self.statusMessage = statusMessage
                self.response = Restful.Response(self.statusCode, self.statusMessage)

            def jsonify(self):
                return self.response.jsonify()

class ErrorHandlers():

    @staticmethod
    def Generic(error):
        response = error.jsonify()
        response.status_code = error.statusCode
        return response

class AuxMethods():

    @staticmethod
    def noCacheHeader(request):
        request.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        request.headers["Pragma"] = "no-cache"
        request.headers["Expires"] = "0"
        return request
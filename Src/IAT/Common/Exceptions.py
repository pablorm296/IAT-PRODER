# Exceptions
class ApiException(Exception):

    status_code = 500

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'IAT-PRODER API exception: {0}'.format(self.message)
        else:
            return 'IAT-PRODER API exception: The API encountered an error. No further details were given.'

class BadRequest(ApiException):

    status_code = 400

    def __str__(self):
        if self.message:
            return 'IAT-PRODER API client side error (HTTP Bad Request): {0}'.format(self.message)
        else:
            return 'IAT-PRODER API client side error: Bad Request. No further details were given.'

class Unauthorized(ApiException):

    status_code = 401

    def __str__(self):
        if self.message:
            return 'IAT-PRODER API client side error (HTTP Unauthorized): {0}'.format(self.message)
        else:
            return 'IAT-PRODER API client side error: Unauthorized. No further details were given.'

class Forbidden(ApiException):

    status_code = 403

    def __str__(self):
        if self.message:
            return 'IAT-PRODER API client side error (HTTP Forbidden): {0}'.format(self.message)
        else:
            return 'IAT-PRODER API client side error: Forbidden. No further details were given.'

class FrontEndException(Exception):
     
    status_code = 500

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'IAT-PRODER front end exception: {0}'.format(self.message)
        else:
            return 'The app encountered an error. No further details were given.'
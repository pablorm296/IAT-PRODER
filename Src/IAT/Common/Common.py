
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
            return 'IAT-PRODER API Exception: {0}'.format(self.message)
        else:
            return 'The Api encountered an error. No further details were given'

class InvalidCredentials(ApiException):

    status_code = 401

    def __str__(self):
        if self.message:
            return 'IAT-PRODER API Client Side Error (HTTP Unauthorized): {0}'.format(self.message)
        else:
            return 'Client side error: Bad Credentials. User attempted to use an invalid username or password. No further details were given'

class InvalidToken(ApiException):

    status_code = 401

    def __str__(self):
        if self.message:
            return 'IAT-PRODER API Client Side Error (HTTP Unauthorized): {0}'.format(self.message)
        else:
            return 'Client side error: Bad Token. User attempted to use an invalid token. No further details were given'


class BadRequest(ApiException):

    status_code = 400

    def __str__(self):
        if self.message:
            return 'IAT-PRODER API Client Side Error (HTTP Bad Request): {0}'.format(self.message)
        else:
            return 'Client side error: Bad Request. No further details were given'
import flask
import json
import logging
from typing import Union

# Set up logging
logger = logging.getLogger(__name__)

class Response:
    def __init__(self, data: Union[dict, str], status_code: int = 200, error: bool = False, message: str = None):

        # Define response template
        json_body = {
            "meta": {
                "Api": "IAT-PRODER",
                "Version": "1.0"
            }
        }

        # First, check if it's an error
        if error:
            # Check that the message is not empty
            if message is None: 
                logger.warning("Initializing an error response without message!")
                message = "Well... This is embarrasing. The server encountered an undefined error!"
            # Check status code
            if status_code >= 100 or status_code < 600:
                logger.warning("Initializing an error response with a misleading status code")
            # Fill template
            json_body["error"] = message
            # Check data
            if data is not None or data != {}:
                logger.warning("Tried to pass data to an error response. Will ignore it")
                data = {}
        else:
            if type(data) is dict:
                json_body["data"] = data
            elif type(data) is str:
                json_body["message"] = data
            else:
                raise TypeError("Api Responses only accepts 'dict' and 'str' objects", "Invalid response content")

        # Make response
        self.__flaskResponse = flask.make_response((json_body, status_code))
        # Remember if it's an error response
        self.error = error
        self.error_message = message
        # Remember original json
        self.__json_body = json_body

    # Status code property
    @property
    def status_code(self):
        return self.__flaskResponse.status_code

    # Status code setter
    @status_code.setter
    def status_code(self, status_code: int):
        # Check if this response was saved as an error
        if self.error:
            if status_code >= 100 or status_code < 600:
                logger.warning("Setting a misleading status code (this is an error response)")
        # Change status code
        self.__flaskResponse.status_code = status_code

    # json_body property
    @property
    def json_body(self):
        return self.__json_body

    # json_body setter
    @json_body.setter
    def json_body(self, body: dict):
        # Set new json body
        self.__json_body = body

        # Set new body inside response objetc
        body_as_json = json.dumps(body)
        self.__flaskResponse.set_data(body_as_json)

    @property
    def response(self):
        return self.__flaskResponse
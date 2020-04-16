from backend import app
from flask import jsonify


class UserSessionVerification(Exception):
    status_code = 401

    def __init__(self, message, status_code, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

    """
    Error raised if the User's session does not exist. This is suppose to be
    used in conjunction of other decorators
    """
    pass


@app.errorhandler(UserSessionVerification)
def handle_nonexistent_session(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

from flask import request
from backend.hints.schemas import hint_form_schema
from backend.models import Hint
from functools import wraps


# Decorator to check if a hint exists
def hint_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        hint = Hint.query.get(kwargs['hint_id'])

        if hint:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Hint does not exist"
                   }, 404

    return wrap


# Decorator to check if a hint exists in github
def hint_exists_in_github(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        hint = Hint.query.filter_by(filename=data["filename"]).first()

        if hint:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Hint does not exist"
                   }, 404

    return wrap


# Decorator to validate hint form data
def valid_hint_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        errors = hint_form_schema.validate(data)

        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a hint. Double check the JSON data that it has everything needed to create a hint."
                   }, 500
        else:
            return f(*args, **kwargs)

    return wrap

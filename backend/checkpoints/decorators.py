from flask import request
from backend.checkpoints.schemas import checkpoint_form_schema
from backend.models import Checkpoint
from functools import wraps


# Decorator to check if a checkpoint exists
def checkpoint_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        checkpoint = Checkpoint.query.get(kwargs['checkpoint_id'])

        if checkpoint:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Checkpoint does not exist"
                   }, 404

    return wrap


# Decorator to check if a checkpoint exists in github
def checkpoint_exists_in_github(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        checkpoint = Checkpoint.query.filter_by(filename=data["filename"]).first()

        if checkpoint:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Checkpoint does not exist"
                   }, 404

    return wrap


# Decorator to validate checkpoint form data
def valid_checkpoint_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        errors = checkpoint_form_schema.validate(data)

        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a checkpoint. Double check the JSON data that it has everything needed to create a checkpoint."
                   }, 500
        else:
            return f(*args, **kwargs)

    return wrap

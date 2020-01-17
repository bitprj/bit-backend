from flask import request
from backend import contentful_client
from backend.config import SPACE_ID
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


# Decorator to check if a checkpoint exists in contentful
def checkpoint_exists_in_contentful(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        content_type = data["contentType"]["sys"]["id"]
        checkpoint = Checkpoint.query.filter_by(contentful_id=data["entityId"]).first()
        contentful_checkpoint = contentful_client.entries(SPACE_ID, 'master').find(data["entityId"])
        # Checks if the checkpoint exists in contentful and if its a checkpoint
        # Checks if the checkpoint exists in the db for put request
        if contentful_checkpoint and content_type == "checkpoint" or checkpoint:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Checkpoint does not exist"
                   }, 404

    return wrap


# Decorator to check if the checkpoint can be deleted
def checkpoint_delete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        checkpoint = Checkpoint.query.filter_by(contentful_id=data["entityId"]).first()

        if checkpoint:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Checkpoint does not exist"
                   }, 404

    return wrap

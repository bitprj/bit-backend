from flask import request
from flask_jwt_extended import get_jwt_identity
from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Checkpoint, CheckpointProgress, Student
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


# Decorator to check if the checkpoint progress exist
def checkpoint_progress_exist(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        checkpoint_prog = CheckpointProgress.query.filter_by(checkpoint_id=kwargs['checkpoint_id'],
                                                             student_id=student.id).first()
        if checkpoint_prog:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Checkpoint progress does not exist"
                   }, 404

    return wrap

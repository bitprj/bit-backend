from backend.checkpoint_progresses.schemas import checkpoint_submission_schema
from backend.models import CheckpointProgress
from flask import request, session
from functools import wraps


# Decorator to check if the checkpoint progress exist
def checkpoint_progress_exist(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_data = session["profile"]
        checkpoint_prog = CheckpointProgress.query.filter_by(checkpoint_id=kwargs['checkpoint_id'],
                                                             student_id=user_data["student_id"]).first()
        if checkpoint_prog:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Checkpoint progress does not exist"
                   }, 404

    return wrap


# Decorator to check if the checkpoint progress has been completed
def multiple_choice_is_completed(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_data = session["profile"]
        checkpoint_prog = CheckpointProgress.query.filter_by(checkpoint_id=kwargs['checkpoint_id'],
                                                             student_id=user_data["student_id"]).first()

        if checkpoint_prog.is_completed and checkpoint_prog.checkpoint.checkpoint_type == "Multiple Choice":
            return {
                       "message": "You already answered this multiple choice checkpoint"
                   }, 500
        else:
            return f(*args, **kwargs)

    return wrap


# Decorator to validate the data being sent for completing a checkpoint progress
def valid_checkpoint_progress_data(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        content_data = request.form
        files = request.files
        data = {}

        if "content" in content_data:
            data["content"] = content_data["content"]
        elif "content" in files:
            data["content"] = request.files
            data["comment"] = content_data["comment"]

        errors = checkpoint_submission_schema.validate(data)

        if errors:
            return {
                       "message": "Incorrect data being sent over"
                   }, 422
        else:
            return f(*args, **kwargs)

    return wrap

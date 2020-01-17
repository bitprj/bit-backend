from flask import request
from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Step
from functools import wraps


# Decorator to check if a step exists
def step_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        step = Step.query.get(kwargs['step_id'])

        if step:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Step does not exist"
                   }, 404

    return wrap


# Decorator to check if a step exists in contentful
def step_exists_in_contentful(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        content_type = data["contentType"]["sys"]["id"]
        step = Step.query.filter_by(contentful_id=data["entityId"]).first()
        contentful_step = contentful_client.entries(SPACE_ID, 'master').find(data["entityId"])
        # Checks if the step exists in contentful and if its a step
        # Checks if the step exists in the db for put request
        if contentful_step and content_type == "step" or step:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Step does not exist"
                   }, 404

    return wrap


# Decorator to check if the step can be deleted
def step_delete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        step = Step.query.filter_by(contentful_id=data["entityId"]).first()

        if step:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Step does not exist"
                   }, 404

    return wrap

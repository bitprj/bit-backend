from flask import request
from backend.steps.schemas import step_form_schema
from backend.steps.utils import get_step_from_patent
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


# Decorator to check if a step exists in github
def step_exists_in_github(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        step = get_step_from_patent(data)

        if step:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Step does not exist"
                   }, 404

    return wrap


# Decorator to validate step form data
def valid_step_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        errors = step_form_schema.validate(data)
        # print(data["step_key"])
        # print(data)
        # print(errors)

        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a step. Double check the JSON data that it has everything needed to create a step."
                   }, 500
        else:
            return f(*args, **kwargs)

    return wrap

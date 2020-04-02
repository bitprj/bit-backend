from flask import request
from backend.activities.schemas import activity_form_schema
from backend.models import Activity
from functools import wraps


# Decorator to check if a activity exists
def activity_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        activity = Activity.query.get(kwargs['activity_id'])

        if activity:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Activity does not exist"
                   }, 404

    return wrap


# Decorator to check if an activity project exists
def activity_project_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        activity = Activity.query.get(data['chosen_project_id'])

        if activity:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Project does not exist"
                   }, 404

    return wrap


# Decorator to check if a module exists in github
def activity_exists_in_github(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        activity = Activity.query.filter_by(filename=data["filename"]).first()

        if activity:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Activity does not exist"
                   }, 404

    return wrap


# Decorator to validate activity form data
def valid_activity_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        errors = activity_form_schema.validate(data)

        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a activity. Double check the JSON data that it has everything needed to create a activity."
                   }, 500
        else:
            return f(*args, **kwargs)

    return wrap

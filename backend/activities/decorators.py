from flask import request
from flask_jwt_extended import get_jwt_identity
from backend.activities.schemas import activity_form_schema
from backend.models import Activity, Student
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


# Decorator to check if a module exists in github
def activity_exists_in_github(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        activity = Activity.query.filter_by(github_id=data["github_id"]).first()

        if activity:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Activity does not exist"
                   }, 404

    return wrap


# Decorator to check if a activity exists in contentful
def activity_exists_in_student_prog(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        activity_completed = request.get_json()
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        activity_id = activity_completed["complete"]["id"]
        activity = Activity.query.get(activity_id)

        if activity:
            if activity in student.current_activities:
                return f(*args, **kwargs)
            else:
                return {
                           "message": "Activity not in student's incomplete_activities"
                       }, 500
        else:
            return {
                       "message": "Activity does not exist"
                   }, 500

    return wrap


# Decorator to validate activity form data
def valid_activity_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        errors = activity_form_schema.validate(data)
        print(errors)
        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a activity. Double check the JSON data that it has everything needed to create a activity."
                   }, 500
        else:
            return f(*args, **kwargs)

    return wrap

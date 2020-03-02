from flask import request
from flask_jwt_extended import get_jwt_identity
from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Module, Student
from functools import wraps


# Decorator to check if a module exists
def module_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        module = Module.query.get(kwargs['module_id'])

        if module:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Module does not exist"
                   }, 404

    return wrap


# Decorator to check if a module exists in contentful
def module_exists_in_contentful(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        content_type = data["contentType"]["sys"]["id"]
        module = Module.query.filter_by(contentful_id=data["entityId"]).first()
        contentful_module = contentful_client.entries(SPACE_ID, 'master').find(data["entityId"])
        # Checks if the module exists in contentful and if its a module
        # Checks if the module exists in the db for put request
        if contentful_module and content_type == "module" or module:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Module does not exist"
                   }, 404

    return wrap


# Function to check if a module exists in github


# Decorator to check if a module is in the incomplete column
def module_is_incomplete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        module = Module.query.get(kwargs["module_id"])

        if module in student.incomplete_modules:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Module has already been added!"
                   }, 500

    return wrap


# Decorator to check if a module has been completed
def module_in_inprogress(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        module = Module.query.get(kwargs["module_id"])

        if module in student.inprogress_modules:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Module does not exist in the student's incomplete modules."
                   }, 500

    return wrap


# Decorator to check if a module has been completed
def module_is_complete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        module = Module.query.get(kwargs["module_id"])

        for activity in module.activities:
            if activity not in student.completed_activities:
                return {
                           "message": "You are not ready to complete the module yet"
                       }, 500

        return f(*args, **kwargs)

    return wrap

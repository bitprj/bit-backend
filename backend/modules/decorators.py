from backend.classrooms.schemas import classroom_modules_schema
from backend.models import Module, Student
from backend.modules.schemas import module_form_schema
from backend.modules.utils import get_modules
from flask import request, session
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


# Decorator to check if a module exists in github
def module_exists_in_github(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        module = Module.query.filter_by(filename=data["filename"]).first()

        if module:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Module does not exist"
                   }, 404

    return wrap


# Decorator to check if a module is in the incomplete column
def module_is_incomplete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_data = session["profile"]
        student = Student.query.get(user_data["student_id"])
        module = Module.query.get(kwargs["module_id"])

        if module in student.incomplete_modules:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Module has already been added!"
                   }, 500

    return wrap


# Decorator to check if a module is in progress
def module_in_inprogress(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_data = session["profile"]
        student = Student.query.get(user_data["student_id"])
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
        user_data = session["profile"]
        student = Student.query.get(user_data["student_id"])
        module = Module.query.get(kwargs["module_id"])

        for activity in module.activities:
            if activity not in student.completed_activities:
                return {
                           "message": "You are not ready to complete the module yet"
                       }, 500

        return f(*args, **kwargs)

    return wrap


# Decorator to validate module form data
def valid_module_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        errors = module_form_schema.validate(data)

        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a module. Double check the JSON data that it has everything needed to create a module."
                   }, 422
        else:
            return f(*args, **kwargs)

    return wrap


# Decorator to check if a list of modules is valid
def valid_modules_list(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        errors = classroom_modules_schema.validate(data)

        if errors:
            return {
                "message": "Incorrect data types in list"
            }, 422
        else:
            modules = get_modules(data["module_ids"])

            if None in modules:
                return {
                           "message": "Invalid module in list"
                       }, 422
            else:
                return f(*args, **kwargs)

    return wrap

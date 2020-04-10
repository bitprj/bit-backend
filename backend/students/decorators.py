from backend.models import Student
from backend.students.schemas import update_data_schema
from flask import request, session
from functools import wraps


# Decorator to check if the user is logged in
def student_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if request.args:
            student_id = request.args.get("student_id")
            student = Student.query.get(student_id)

            if student and student_id:
                return f(*args, **kwargs)
            else:
                return {
                           "message": "Student does not exist"
                       }, 404
        else:
            user_data = session["profile"]
            student = Student.query.get(user_data["id"])

            if student:
                return f(*args, **kwargs)
            else:
                return {
                           "message": "Student does not exist"
                       }, 404

    return wrap


# Decorator to check if the user is logged in
def valid_update_data(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        errors = update_data_schema.validate(data)

        if errors:
            return {
                       "message": "Missing or sending incorrect data"
                   }, 422
        else:
            return f(*args, **kwargs)

    return wrap

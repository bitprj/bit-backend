from backend.models import Student
from backend.students.schemas import update_data_schema
from flask import request
from flask_jwt_extended import get_jwt_identity
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
            username = get_jwt_identity()
            student = Student.query.filter_by(username=username).first()

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

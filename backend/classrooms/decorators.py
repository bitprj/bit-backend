from flask import request
from flask_jwt_extended import get_jwt_identity
from backend.classrooms.schemas import classroom_code_schema, classroom_form_schema
from backend.models import Classroom, Teacher
from functools import wraps


# Decorator to check if a classroom exists
def classroom_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        classroom = Classroom.query.get(kwargs['classroom_id'])

        if classroom:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Classroom does not exist"
                   }, 404

    return wrap


# Decorator to check if a teacher owns a classrooms
def owns_classroom(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        classroom = Classroom.query.get(kwargs['classroom_id'])
        username = get_jwt_identity()
        teacher = Teacher.query.filter_by(username=username).first()

        if classroom.teacher_id == teacher.id:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "You do not own this classroom"
                   }, 203

    return wrap


# Decorator to check if a classroom form data is valid
def valid_classroom_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        form_data = request.get_json()
        errors = classroom_form_schema.validate(form_data)

        # If form data is not validated by the classroom_schema, then return a 500 error
        # else create the classroom and add it to the database
        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a classroom. Double check the JSON data that it has everything needed to create a classroom."
                   }, 500
        else:
            return f(*args, **kwargs)

    return wrap

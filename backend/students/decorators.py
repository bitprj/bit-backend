from backend.models import Student
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

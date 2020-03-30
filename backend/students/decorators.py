from backend.models import Student
from flask import request
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
            return f(*args, **kwargs)

    return wrap

from flask import request
from flask_jwt_extended import get_jwt_identity
from backend.activity_progresses.schemas import activity_progress_grading_schema
from backend.models import ActivityProgress, Student
from functools import wraps


# Decorator to check if a activity exists
def activity_prog_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        student_activity_prog = ActivityProgress.query.filter_by(student_id=student.id,
                                                                 activity_id=kwargs['activity_id']).first()

        if student_activity_prog:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Student activity progress does not exist."
                   }, 404

    return wrap


# Decorator to check if assignments are sent in the right format
def activity_prog_grading_format(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        form_data = request.get_json()
        errors = activity_progress_grading_schema.validate(form_data)

        if not errors:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Assignments are in the wrong format."
                   }, 500

    return wrap


# Decorator to check if assignment exists and can be graded
def submitted_activity_prog_exist(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        form_data = request.get_json()
        student_activity_prog = ActivityProgress.query.get(form_data["activity_progress_id"])

        if student_activity_prog:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Student activity progress does not exist."
                   }, 404

    return wrap

from backend.models import ModuleProgress, Student
from backend.module_progresses.schemas import module_progress_update_data_schema
from flask import request
from flask_jwt_extended import get_jwt_identity
from functools import wraps


# Decorator to check if a module exists
def module_prog_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        module_progress = ModuleProgress.query.filter_by(module_id=kwargs['module_id'], student_id=student.id).first()

        if module_progress:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "ModuleProgress does not exist"
                   }, 404

    return wrap


# Decorator to validate data sent to update ModuleProgress
def valid_update_data(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        errors = module_progress_update_data_schema.validate(data)

        if errors:
            return {
                       "message": "Missing or sending incorrect data"
                   }, 422
        else:
            return f(*args, **kwargs)

    return wrap

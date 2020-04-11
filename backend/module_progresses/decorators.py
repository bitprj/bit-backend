from backend.models import ModuleProgress
from backend.module_progresses.schemas import module_progress_update_data_schema
from flask import request, session
from functools import wraps


# Decorator to check if a module exists
def module_prog_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_data = session["profile"]
        module_progress = ModuleProgress.query.filter_by(module_id=kwargs['module_id'],
                                                         student_id=user_data["id"]).first()

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

from backend.models import Teacher
from functools import wraps


# Decorator to check if the user is logged in
def teacher_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        teacher = Teacher.query.get(kwargs["teacher_id"])

        if teacher:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Teacher does not exist"
                   }, 404

    return wrap

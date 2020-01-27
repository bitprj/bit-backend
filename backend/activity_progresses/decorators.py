from flask_jwt_extended import get_jwt_identity
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

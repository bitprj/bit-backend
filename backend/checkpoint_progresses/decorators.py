from flask_jwt_extended import get_jwt_identity
from backend.models import CheckpointProgress, Student
from functools import wraps


# Decorator to check if the checkpoint progress exist
def checkpoint_progress_exist(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        checkpoint_prog = CheckpointProgress.query.filter_by(checkpoint_id=kwargs['checkpoint_id'],
                                                             student_id=student.id).first()
        if checkpoint_prog:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Checkpoint progress does not exist"
                   }, 404

    return wrap


# Decorator to check if the checkpoint progress has been completed
def checkpoint_progress_is_completed(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        checkpoint_prog = CheckpointProgress.query.filter_by(checkpoint_id=kwargs['checkpoint_id'],
                                                             student_id=student.id).first()
        if checkpoint_prog.is_completed:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Checkpoint progress is not completed"
                   }, 500

    return wrap

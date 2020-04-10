from backend.activity_progresses.schemas import activity_progress_grading_schema
from backend.models import Activity, ActivityProgress
from flask import request, session
from functools import wraps


# Decorator to check if a activity exists
def activity_prog_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_data = session["profile"]
        student_activity_prog = ActivityProgress.query.filter_by(student_id=user_data["id"],
                                                                 activity_id=kwargs['activity_id']).first()

        if student_activity_prog:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Student activity progress does not exist."
                   }, 404

    return wrap


# Decorator to not let Student's do an Activity if they do not satisfy the prerequisites
def has_completed_prerequisites(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_data = session["profile"]
        activity = Activity.query.get(kwargs["activity_id"])

        for activity_prereq in activity.prerequisite_activities:
            activity_prog = ActivityProgress.query.filter_by(student_id=user_data["id"],
                                                             activity_id=activity_prereq.id).first()
            if activity_prog:
                if not activity_prog.is_completed:
                    return {
                               "message": "You do not satisfy the Activity prerequisites"
                           }, 403

        return f(*args, **kwargs)

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


# Decorator to check if an activity has cards
# Activity Progress would fail to be created if cards do not exist
def cards_exist_in_activity(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        activity = Activity.query.get(kwargs["activity_id"])

        if len(activity.cards) > 0:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Activity has no cards. ActivityProgress could not be created"
                   }, 500

    return wrap


# Function to check if an activity has been graded
def is_activity_graded(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        student_activity_prog = ActivityProgress.query.filter_by(activity_id=kwargs["activity_id"],
                                                                 student_id=data["student_id"]).first()

        if not student_activity_prog.is_graded:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Activity has already been graded."
                   }, 403

    return wrap


# Decorator to check if assignment exists and can be graded
def submitted_activity_prog_exist(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        student_activity_prog = ActivityProgress.query.filter_by(activity_id=kwargs["activity_id"],
                                                                 student_id=data["student_id"])

        if student_activity_prog:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Student activity progress does not exist."
                   }, 404

    return wrap

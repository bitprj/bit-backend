from flask import Blueprint
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api, db
from backend.activities.utils import validate_activity
from backend.activity_progresses.schemas import activity_progress_schema
from backend.activity_progresses.utils import create_progress, unlock_hint
from backend.cards.utils import get_cards_hints
from backend.general_utils import get_user_id_from_token
from backend.hints.utils import create_hint_status, validate_hint
from backend.models import ActivityProgress, Hint

# Blueprint for activity progresses
activity_progresses_bp = Blueprint("activity_progresses", __name__)


# Class to handle the activity progress model
class ActivityProgressUpdate(Resource):
    method_decorators = [roles_accepted("Student")]

    # Function to return the last card completed on an activity
    def get(self, activity_id):
        current_user_id = get_user_id_from_token()
        activity_error = validate_activity(activity_id)

        if activity_error:
            return {
                       "message": "Activity does not exist"
                   }, 404

        student_activity_prog = ActivityProgress.query.filter_by(student_id=current_user_id,
                                                                 activity_id=activity_id).first()

        if not student_activity_prog:
            # Create Activity Progress if it does not exist
            activity_prog = create_progress(activity_id, current_user_id)
            db.session.add(activity_prog)
            db.session.commit()

            # Fills in the hints and cards as locked in the activity progress
            hints = get_cards_hints(activity_prog.activity.cards)
            create_hint_status(activity_prog, hints)
            db.session.commit()

            return activity_progress_schema.dump(activity_prog)
        else:
            return activity_progress_schema.dump(student_activity_prog)

    def delete(self, activity_id):
        current_user_id = get_user_id_from_token()
        student_activity_prog = ActivityProgress.query.filter_by(student_id=current_user_id,
                                                                 activity_id=activity_id).first()
        if not student_activity_prog:
            return {
                       "message": "Student activity progress does not exist."
                   }, 500
        else:
            db.session.delete(student_activity_prog)
            db.session.commit()

        return {
                   "message": "Student activity progress successfully deleted."
               }, 200


# Class to handle the activity progress' hints
class ActivityProgressHints(Resource):
    method_decorators = [roles_accepted("Student")]

    # Function to unlock a hint by its hint_id
    def put(self, activity_id, hint_id):
        current_user_id = get_user_id_from_token()
        activity_error = validate_activity(activity_id)

        if activity_error:
            return {
                       "message": "Activity does not exist"
                   }, 404
        else:
            student_activity_prog = ActivityProgress.query.filter_by(student_id=current_user_id,
                                                                     activity_id=activity_id).first()
            if not student_activity_prog:
                return {
                    "message": "Activity progress does not exist"
                }, 404
            else:

                hint_error = validate_hint(hint_id)

                if not hint_error:
                    return {
                               "message": "Hint does not exist"
                           }, 404
                else:
                    hint = Hint.query.get(hint_id)

                    unlock_message = unlock_hint(student_activity_prog, hint)
                    db.session.commit()

                    return {
                               "message": unlock_message
                           }, 200


# Creates the routes for the classes
api.add_resource(ActivityProgressUpdate, "/activities/<int:activity_id>/progress")
api.add_resource(ActivityProgressHints, "/activities/<int:activity_id>/hints/<int:hint_id>")

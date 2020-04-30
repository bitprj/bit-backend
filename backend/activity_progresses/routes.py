from backend import api, db
from backend.authentication.decorators import roles_accepted, user_session_exists
from backend.activities.decorators import activity_exists
from backend.activity_progresses.decorators import activity_prog_exists, cards_exist_in_activity, \
    has_completed_prerequisites
from backend.activity_progresses.schemas import activity_progress_schema
from backend.activity_progresses.utils import create_progress, fill_in_rels, unlock_hint
from backend.hints.decorators import hint_exists
from backend.models import ActivityProgress, Card, Hint, Student
from backend.students.utils import update_module_progresses, update_topic_progresses
from flask import Blueprint, session
from flask_restful import Resource

# Blueprint for activity progresses
activity_progresses_bp = Blueprint("activity_progresses", __name__)


# Class to handle the activity progress model
class ActivityProgressUpdate(Resource):
    method_decorators = [user_session_exists, roles_accepted("Student")]

    # Function to return the last card completed on an activity
    @cards_exist_in_activity
    # @has_completed_prerequisites
    def get(self, activity_id):
        user_data = session["profile"]
        student = Student.query.get(user_data["student_id"])
        student_activity_prog = ActivityProgress.query.filter_by(student_id=student.id,
                                                                 activity_id=activity_id).first()

        if not student_activity_prog:
            # Create Activity Progress if it does not exist
            student_activity_prog = create_progress(activity_id, student.id)
            student.current_activities.append(student_activity_prog.activity)
            fill_in_rels(student_activity_prog, student)
            # TODO edit the relationship function later
            topics = update_module_progresses(student_activity_prog.activity, student)
            update_topic_progresses(topics, student)

        card = Card.query.get(student_activity_prog.last_card_unlocked)
        progress = activity_progress_schema.dump(student_activity_prog)
        progress["last_card_unlocked_id"] = card.id
        db.session.commit()

        return progress

    @activity_prog_exists
    def delete(self, activity_id):
        user_data = session["profile"]
        student_activity_prog = ActivityProgress.query.filter_by(student_id=user_data["student_id"],
                                                                 activity_id=activity_id).first()
        db.session.delete(student_activity_prog)
        db.session.commit()

        return {
                   "message": "Student activity progress successfully deleted."
               }, 200


# Class to handle the activity progress' hints
class ActivityProgressHints(Resource):
    method_decorators = [user_session_exists, roles_accepted("Student"), activity_exists, hint_exists]

    # Function to unlock a hint by its hint_id
    @activity_prog_exists
    def put(self, activity_id, hint_id):
        user_data = session["profile"]
        student_activity_prog = ActivityProgress.query.filter_by(student_id=user_data["student_id"],
                                                                 activity_id=activity_id).first()
        hint = Hint.query.get(hint_id)
        unlock_message = unlock_hint(student_activity_prog, hint)

        db.session.commit()

        return {
                   "message": unlock_message
               }, 200


# Creates the routes for the classes
api.add_resource(ActivityProgressUpdate, "/activities/<int:activity_id>/progress")
api.add_resource(ActivityProgressHints, "/activities/<int:activity_id>/hints/<int:hint_id>")

from flask import Blueprint
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.activities.decorators import activity_exists
from backend.activity_progresses.decorators import activity_prog_exists, cards_exist_in_activity
from backend.activity_progresses.schemas import activity_progress_schema
from backend.activity_progresses.utils import create_progress, unlock_hint
from backend.cards.utils import get_cards_hints
from backend.hints.decorators import hint_exists
from backend.hints.utils import create_hint_status
from backend.models import ActivityProgress, Card, Hint, Student

# Blueprint for activity progresses
activity_progresses_bp = Blueprint("activity_progresses", __name__)


# Class to handle the activity progress model
class ActivityProgressUpdate(Resource):
    method_decorators = [roles_accepted("Student"), activity_exists]

    # Function to return the last card completed on an activity
    @cards_exist_in_activity
    def get(self, activity_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        student_activity_prog = ActivityProgress.query.filter_by(student_id=student.id,
                                                                 activity_id=activity_id).first()

        if not student_activity_prog:
            # Create Activity Progress if it does not exist
            student_activity_prog = create_progress(activity_id, student.id)
            student.current_activities.append(student_activity_prog.activity)

            if student_activity_prog.activity in student.incomplete_activities:
                student.incomplete_activities.remove(student_activity_prog.activity)

            db.session.add(student_activity_prog)
            db.session.commit()

            # Fills in the hints and cards as locked in the activity progress
            hints = get_cards_hints(student_activity_prog.activity.cards)
            create_hint_status(student_activity_prog, hints)
            db.session.commit()

        card = Card.query.get(student_activity_prog.last_card_unlocked)
        progress = activity_progress_schema.dump(student_activity_prog)
        progress["card_contentful_id"] = card.contentful_id

        return progress

    @activity_prog_exists
    def delete(self, activity_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        student_activity_prog = ActivityProgress.query.filter_by(student_id=student.id,
                                                                 activity_id=activity_id).first()
        db.session.delete(student_activity_prog)
        db.session.commit()

        return {
                   "message": "Student activity progress successfully deleted."
               }, 200


# Class to handle the activity progress' hints
class ActivityProgressHints(Resource):
    method_decorators = [roles_accepted("Student"), activity_exists, hint_exists]

    # Function to unlock a hint by its hint_id
    @activity_prog_exists
    def put(self, activity_id, hint_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        student_activity_prog = ActivityProgress.query.filter_by(student_id=student.id,
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

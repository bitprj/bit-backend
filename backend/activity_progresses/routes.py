from flask import Blueprint, request
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api, db
from backend.activities.utils import validate_activity
from backend.activity_progresses.schemas import activity_progress_card_hints, activity_progress_schema, \
    activity_progress_video
from backend.activity_progresses.utils import create_progress, get_hint_data, unlock_card
from backend.general_utils import get_user_id_from_token
from backend.models import ActivityProgress

# Blueprint for activity progresses
activity_progresses_bp = Blueprint("activity_progresses", __name__)


# Class to submit a student's video
class ActivityProgressSubmit(Resource):
    method_decorators = [roles_accepted("Student")]

    # Function to submit a student's video
    def post(self, activity_id):
        submission_data = request.get_json()
        current_user_id = get_user_id_from_token()
        video_error = activity_progress_video.validate(submission_data)
        student_activity_prog = ActivityProgress.query.filter_by(student_id=current_user_id,
                                                                 activity_id=activity_id).first()
        if video_error:
            return {
                       "message": "Missing or sending incorrect data to create an activity. Double check the JSON data that it has everything needed to create an activity."
                   }, 500
        else:
            if not student_activity_prog:
                return {
                           "message": "Student activity progress does not exist."
                       }, 500

            student_activity_prog.video = submission_data["video"]
            db.session.commit()

        return {
                   "message": "Submission video has been submitted!"
               }, 201


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

            return activity_progress_schema.dump(activity_prog)
        else:
            return activity_progress_schema.dump(student_activity_prog)

    # Function to submit a student's activity progress
    def put(self, activity_id):
        current_user_id = get_user_id_from_token()
        student_activity_prog = ActivityProgress.query.filter_by(student_id=current_user_id,
                                                                 activity_id=activity_id).first()
        if student_activity_prog.cards_locked:
            target_card = unlock_card(student_activity_prog)
            hints = get_hint_data(student_activity_prog, target_card)
            return activity_progress_card_hints.dump(hints)

        return {
                   "message": "No more cards to unlock!"
               }, 201

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


# Creates the routes for the classes
api.add_resource(ActivityProgressSubmit, "/activities/<int:activity_id>/submit")
api.add_resource(ActivityProgressUpdate, "/activities/<int:activity_id>/progress")

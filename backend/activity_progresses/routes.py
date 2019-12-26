from flask import Blueprint, request
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api, db
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
        student_activity_prog = ActivityProgress.query.filter_by(student_id=current_user_id,
                                                                 activity_id=activity_id).first()

        if not student_activity_prog:
            return {
                       "message": "Student activity progress does not exist."
                   }, 500
        else:
            student_activity_prog.video = submission_data["video"]

        return {
                   "message": "Submission video has been submitted!"
               }, 201


# Class to handle the activity progress model
class ActivityProgressUpdate(Resource):
    method_decorators = [roles_accepted("Student")]

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

from flask import Blueprint, request
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api, db
from backend.activity_progresses.schemas import activity_progress_submission_schema, activity_progress_grading_schema
from backend.classrooms.utils import owns_classroom, validate_classroom
from backend.general_utils import get_user_id_from_token
from backend.models import ActivityProgress, Classroom
from backend.teachers.utils import assign_comments, get_activities, pusher_activity
from datetime import datetime

# Blueprint for teachers
teachers_bp = Blueprint("teachers", __name__)


# Class to display teacher data
class TeacherAssignments(Resource):
    method_decorators = [roles_accepted("Teacher")]

    # Function to display teacher data
    def get(self, classroom_id):
        current_user_id = get_user_id_from_token()
        classroom_error = validate_classroom(classroom_id)

        if classroom_error:
            return {
                       "message": "Classroom does not exist"
                   }, 404
        else:
            teacher_owns_class = owns_classroom(classroom_id, current_user_id)

            if not teacher_owns_class:
                return {
                           "message": "You do not own this classroom"
                       }, 500
            else:
                classroom = Classroom.query.get(classroom_id)
                ungraded_assignments = get_activities(classroom)

                if ungraded_assignments:
                    return activity_progress_submission_schema.dump(ungraded_assignments)

        return {
                   "message": "No submitted activities"
               }, 200

    # This route is used to grade an activity
    def put(self, classroom_id):
        current_user_id = get_user_id_from_token()
        classroom_error = validate_classroom(classroom_id)

        if classroom_error:
            return {
                       "message": "Classroom does not exist"
                   }, 404
        else:
            teacher_owns_class = owns_classroom(classroom_id, current_user_id)

            if not teacher_owns_class:
                return {
                           "message": "You do not own this classroom"
                       }, 500
            else:
                form_data = request.get_json()
                errors = activity_progress_grading_schema.validate(form_data)

                if errors:
                    return {
                               "message": "Missing or sending incorrect data to create a classroom. Double check the JSON data that it has everything needed to create a classroom."
                           }, 500
                else:
                    activity_progress = ActivityProgress.query.get(form_data["activity_progress_id"])
                    assign_comments(form_data["checkpoints_failed"])
                    assign_comments(form_data["checkpoints_passed"])
                    
                    if form_data["checkpoints_failed"]:
                        activity_progress.is_passed = False
                    else:
                        activity_progress.is_passed = True

                    activity_progress.is_graded = True
                    activity_progress.date_graded = datetime.now().date()
                    db.session.commit()

                    pusher_activity(activity_progress)

        return {
                   "message": "Student Activity has been graded"
               }, 200


# Creates the routes for the classes
api.add_resource(TeacherAssignments, "/teachers/<int:classroom_id>/grade")

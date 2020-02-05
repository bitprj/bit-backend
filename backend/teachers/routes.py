from flask import Blueprint, request
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.authentication.utils import send_graded_activity_email
from backend.activity_progresses.decorators import activity_prog_grading_format, submitted_activity_prog_exist
from backend.activity_progresses.schemas import activity_progress_submission_schema
from backend.classrooms.decorators import classroom_exists, owns_classroom
from backend.models import ActivityProgress, Classroom, ModuleProgress
from backend.teachers.utils import assign_comments, get_activities, pusher_activity
from datetime import datetime

# Blueprint for teachers
teachers_bp = Blueprint("teachers", __name__)


# Class to display teacher data
class TeacherAssignments(Resource):
    method_decorators = [roles_accepted("Teacher"), classroom_exists]

    # Function to display teacher data
    @owns_classroom
    def get(self, classroom_id):
        classroom = Classroom.query.get(classroom_id)
        ungraded_assignments = get_activities(classroom)

        if ungraded_assignments:
            return activity_progress_submission_schema.dump(ungraded_assignments)

        return {
                   "message": "No submitted activities"
               }, 200

    # This route is used to grade an activity
    @owns_classroom
    @activity_prog_grading_format
    @submitted_activity_prog_exist
    def put(self, classroom_id):
        form_data = request.get_json()
        activity_progress = ActivityProgress.query.get(form_data["activity_progress_id"])
        assign_comments(form_data["checkpoints_failed"])
        assign_comments(form_data["checkpoints_passed"])

        if form_data["checkpoints_failed"]:
            activity_progress.is_passed = False
        else:
            activity_progress.is_passed = True

        activity_progress.is_graded = True
        activity_progress.date_graded = datetime.now().date()

        for module in activity_progress.activity.modules:
            module_prog = ModuleProgress.query.filter_by(module_id=module.id,
                                                         student_id=activity_progress.student.id).first()
            module_prog += activity_progress.accumulated_gems

        db.session.commit()

        send_graded_activity_email(activity_progress.student.username)
        pusher_activity(activity_progress)

        return {
                   "message": "Student Activity has been graded"
               }, 200


# Creates the routes for the classes
api.add_resource(TeacherAssignments, "/teachers/<int:classroom_id>/grade")

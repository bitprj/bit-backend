from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.authentication.utils import send_graded_activity_email
from backend.activity_progresses.decorators import activity_prog_grading_format, is_activity_graded, \
    submitted_activity_prog_exist
from backend.activity_progresses.schemas import activity_progress_submission_schema
from backend.classrooms.decorators import classroom_exists, owns_classroom
from backend.models import ActivityProgress, Classroom, Teacher
from backend.modules.utils import complete_modules
from backend.teachers.schemas import teacher_classroom_schema
from backend.teachers.utils import get_activities, grade_activity, pusher_activity

# Blueprint for teachers
teachers_bp = Blueprint("teachers", __name__)


# Class to retrieve Teacher Data
class TeacherData(Resource):
    method_decorators = [roles_accepted("Teacher")]

    def get(self):
        username = get_jwt_identity()
        teacher = Teacher.query.filter_by(username=username).first()

        return teacher_classroom_schema.dump(teacher)


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
    @is_activity_graded
    def put(self, classroom_id):
        form_data = request.get_json()
        activity_progress = ActivityProgress.query.get(form_data["activity_progress_id"])
        modules_completed = grade_activity(activity_progress, form_data)
        complete_modules(modules_completed)
        db.session.commit()

        send_graded_activity_email(activity_progress.student.username)
        pusher_activity(activity_progress)

        return {
                   "message": "Student Activity has been graded"
               }, 200


# Creates the routes for the classes
api.add_resource(TeacherAssignments, "/teachers/<int:classroom_id>/grade")
api.add_resource(TeacherData, "/teachers/data")

from backend import api, db
from backend.authentication.decorators import user_session_exists, roles_required
from backend.activity_progresses.decorators import activity_prog_grading_format, is_activity_graded, \
    submitted_activity_prog_exist
from backend.models import ActivityProgress, Teacher
from backend.modules.utils import complete_modules
from backend.teachers.decorators import teacher_exists
from backend.teachers.schemas import TeacherSerializer
from backend.teachers.utils import grade_activity
from flask import Blueprint, request
from flask_restful import Resource

# Blueprint for teachers
teachers_bp = Blueprint("teachers", __name__)


# Class to fetch classroom data for the teacher
class TeacherFetchData(Resource):
    method_decorators = [teacher_exists]

    def get(self, teacher_id):
        teacher = Teacher.query.get(teacher_id)

        return TeacherSerializer(teacher).data


# Class to grade the Student's assignments
class TeacherAssignments(Resource):
    method_decorators = [user_session_exists, roles_required("Teacher")]

    # This route is used to grade an activity
    @activity_prog_grading_format
    @submitted_activity_prog_exist
    @is_activity_graded
    def put(self, activity_id):
        data = request.get_json()
        activity_progress = ActivityProgress.query.filter_by(activity_id=activity_id,
                                                             student_id=data["student_id"]).first()
        grade_activity(activity_progress, data)
        complete_modules(activity_progress)
        db.session.commit()

        # send_graded_activity_email(activity_progress.student.username)
        # pusher_activity(activity_progress)

        return {
                   "message": "Student Activity has been graded"
               }, 200


# Creates the routes for the classes
api.add_resource(TeacherAssignments, "/teachers/<int:activity_id>/grade")
api.add_resource(TeacherFetchData, "/teachers/<int:teacher_id>")

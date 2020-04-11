from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.activity_progresses.decorators import activity_prog_grading_format, is_activity_graded, \
    submitted_activity_prog_exist
from backend.models import ActivityProgress, Teacher
from backend.modules.utils import complete_modules
from backend.teachers.schemas import teacher_classroom_schema
from backend.teachers.utils import grade_activity
from flask import Blueprint, request, session
from flask_restful import Resource


# Blueprint for teachers
teachers_bp = Blueprint("teachers", __name__)


# Class to fetch classroom data for the teacher
class TeacherFetchData(Resource):
    method_decorators = [roles_accepted("Teacher")]

    def get(self):
        user_data = session["profile"]
        teacher = Teacher.query.get(user_data["id"])

        return teacher_classroom_schema.dump(teacher)


# Class to display teacher data
class TeacherAssignments(Resource):

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
api.add_resource(TeacherFetchData, "/teachers/data")

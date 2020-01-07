from flask import Blueprint
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api
from backend.activity_progresses.schemas import activity_progress_grading_schema
from backend.classrooms.utils import owns_classroom, validate_classroom
from backend.general_utils import get_user_id_from_token
from backend.models import Classroom
from backend.teachers.utils import get_activities

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
                    return activity_progress_grading_schema.dump(ungraded_assignments)

        return {
                   "message": "No submitted activities"
               }, 200


# Creates the routes for the classes
api.add_resource(TeacherAssignments, "/teachers/<int:classroom_id>/grade")

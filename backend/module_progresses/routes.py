from flask import (Blueprint, request)
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource
from backend import api, db
from backend.activities.decorators import activity_exists_in_student_prog
from backend.authentication.decorators import roles_required
from backend.modules.decorators import module_exists
from backend.modules.utils import get_module_progress
from backend.module_progresses.schemas import module_progress_schema
from backend.models import Activity, Student

# Blueprint for modules
module_progresses_bp = Blueprint("module_progresses", __name__)


# Class for module progress
class ModuleProgress(Resource):
    method_decorators = [roles_required("Student"), module_exists]

    # Function to display a student's module progress
    def get(self, module_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        module_progress = get_module_progress(student, module_id)

        return module_progress_schema.dump(module_progress)

    # Function to update a student's completed_modules
    @activity_exists_in_student_prog
    def put(self):
        activity_completed = request.get_json()
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        activity_id = activity_completed["complete"]["id"]
        activity = Activity.query.get(activity_id)
        student.completed_activities.append(activity)
        student.incomplete_activities.remove(activity)

        db.session.commit()

        return {
                   "message": "Student's module progress successfully updated"
               }, 202


api.add_resource(ModuleProgress, "/modules/<int:module_id>/progress")

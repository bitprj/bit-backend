from backend import api, db
from backend.activities.decorators import activity_project_exists
from backend.authentication.decorators import roles_required
from backend.module_progresses.decorators import module_prog_exists, valid_update_data
from backend.module_progresses.schemas import module_progress_schema
from backend.models import ModuleProgress, Student
from flask import (Blueprint, request)
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource

# Blueprint for modules
module_progresses_bp = Blueprint("module_progresses", __name__)


# Class for module progress
class ModuleProgressData(Resource):
    method_decorators = [roles_required("Student")]

    # Function to display a student's module progress
    @module_prog_exists
    def get(self, module_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        module_progress = ModuleProgress.query.filter_by(module_id=module_id, student_id=student.id).first()

        return module_progress_schema.dump(module_progress)

    # Function to update a student's completed activities
    @module_prog_exists
    @valid_update_data
    @activity_project_exists
    def put(self, module_id):
        data = request.get_json()
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        module_progress = ModuleProgress.query.filter_by(module_id=module_id, student_id=student.id).first()
        module_progress.chosen_project_id = data["chosen_project_id"]
        db.session.commit()

        return module_progress_schema.dump(module_progress)


api.add_resource(ModuleProgressData, "/modules/<int:module_id>/progress")

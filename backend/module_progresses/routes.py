from backend import api, db
from backend.activities.decorators import activity_project_exists
from backend.authentication.decorators import roles_required, valid_token
from backend.module_progresses.decorators import module_prog_exists, valid_update_data
from backend.module_progresses.schemas import ModuleProgressSerializer
from backend.models import ModuleProgress
from flask import (Blueprint, request)
from flask_jwt_extended import get_jwt_claims
from flask_restful import Resource

# Blueprint for modules
module_progresses_bp = Blueprint("module_progresses", __name__)


# Class for module progress
class ModuleProgressData(Resource):
    method_decorators = [roles_required("Student")]

    # Function to display a student's module progress
    @valid_token
    @module_prog_exists
    def get(self, module_id):
        user_data = get_jwt_claims()
        module_progress = ModuleProgress.query.filter_by(module_id=module_id, student_id=user_data["id"]).first()

        return ModuleProgressSerializer(module_progress).data

    # Function to update a student's completed activities
    @valid_token
    @module_prog_exists
    @valid_update_data
    @activity_project_exists
    def put(self, module_id):
        data = request.get_json()
        user_data = get_jwt_claims()
        module_progress = ModuleProgress.query.filter_by(module_id=module_id, student_id=user_data["id"]).first()
        module_progress.chosen_project_id = data["chosen_project_id"]
        db.session.commit()

        return ModuleProgressSerializer(module_progress).data


api.add_resource(ModuleProgressData, "/modules/<int:module_id>/progress")

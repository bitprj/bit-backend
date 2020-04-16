from backend import api, db
from backend.activities.decorators import activity_projects_exists
from backend.authentication.decorators import roles_required
from backend.module_progresses.decorators import module_prog_exists, valid_update_data
from backend.module_progresses.schemas import ModuleProgressSerializer
from backend.module_progresses.utils import update_chosen_projects
from backend.models import ModuleProgress
from flask import Blueprint, request, session
from flask_restful import Resource

# Blueprint for modules
module_progresses_bp = Blueprint("module_progresses", __name__)


# Class for module progress
class ModuleProgressData(Resource):
    method_decorators = [roles_required("Student"), module_prog_exists]

    # Function to display a student's module progress
    def get(self, module_id):
        user_data = session["profile"]
        module_progress = ModuleProgress.query.filter_by(module_id=module_id,
                                                         student_id=user_data["student_id"]).first()

        return ModuleProgressSerializer(module_progress).data

    # Function to update a student's completed activities
    @valid_update_data
    @activity_projects_exists
    def put(self, module_id):
        data = request.get_json()
        user_data = session["profile"]
        module_progress = ModuleProgress.query.filter_by(module_id=module_id,
                                                         student_id=user_data["student_id"]).first()
        module_progress.chosen_projects = update_chosen_projects(data["chosen_project_ids"])
        db.session.commit()

        return ModuleProgressSerializer(module_progress).data


api.add_resource(ModuleProgressData, "/modules/<int:module_id>/progress")

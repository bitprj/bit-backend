from flask import (Blueprint, request)
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api, db
from backend.general_utils import get_user_id_from_token
from backend.modules.schemas import module_schema, module_progress_schema
from backend.modules.utils import create_module, edit_module, get_module_progress, validate_module
from backend.models import Activity, Module, Student

# Blueprint for modules
modules_bp = Blueprint("modules", __name__)


# Class for module CRUD routes
class ModuleCRUD(Resource):
    # Function to create a module
    def post(self):
        contentful_data = request.get_json()
        module = create_module(contentful_data)

        db.session.add(module)
        db.session.commit()

        return {"message": "Module successfully created"}, 201

    # Function to edit an module
    def put(self):
        contentful_data = request.get_json()
        module = Module.query.filter_by(contentful_id=contentful_data["entityId"]).first()

        if not module:
            return {"message": "Module does not exist"}, 404

        edit_module(module, contentful_data)

        db.session.commit()

        return {"message": "Module successfully updated"}, 200


# Function to get a specific Module based on module id
class ModuleGetSpecific(Resource):
    def get(self, module_id):
        module = Module.query.get(module_id)

        if not module:
            return {"message": "Module does not exist"}, 404

        return module_schema.dump(module)


# This class is used to delete an module with a POST request
class ModuleDelete(Resource):
    # Function to delete a module!!
    def post(self):
        contentful_data = request.get_json()
        module = Module.query.filter_by(contentful_id=contentful_data["entityId"]).first()

        if not module:
            return {"message": "Module does not exist"}, 404

        db.session.delete(module)
        db.session.commit()

        return {"message": "Module successfully deleted"}, 200


# Class for module progress
class ModuleProgress(Resource):
    method_decorators = [roles_accepted("Student")]

    # Function to display a student's module progress
    def get(self, module_id):
        current_user_id = get_user_id_from_token()
        module_error = validate_module(module_id)

        if module_error:
            return {
                       "message": "Module does not exist"
                   }, 500
        else:
            module_progress = get_module_progress(current_user_id, module_id)

            return module_progress_schema.dump(module_progress)

    # Function to update a student's completed_modules
    def put(self, module_id):
        current_user_id = get_user_id_from_token()
        student = Student.query.get(current_user_id)
        activity_completed = request.get_json()
        activity_id = activity_completed["complete"]["id"]
        module_error = validate_module(module_id)

        if module_error or activity_error:
            return {
                       "message": "Module or Activity does not exist"
                   }, 500
        else:
            activity = Activity.query.get(activity_id)
            student.completed_activities.append(activity)

            if activity not in student.incomplete_activities:
                return {
                           "message": "Activity not in student's incomplete_activities"
                       }, 500
            else:
                student.incomplete_activities.remove(activity)
                db.session.commit()

        return {
                   "message": "Student's module progress successfully updated"
               }, 202


# Creates the routes for the classes
api.add_resource(ModuleCRUD, "/modules")
api.add_resource(ModuleDelete, "/modules/delete")
api.add_resource(ModuleGetSpecific, "/modules/<int:module_id>")
api.add_resource(ModuleProgress, "/modules/<int:module_id>/progress")

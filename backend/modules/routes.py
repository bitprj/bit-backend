from flask import (Blueprint, request)
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api, db
from backend.activities.utils import validate_activity
from backend.general_utils import get_user_id_from_token
from backend.modules.schemas import module_form_schema, module_schema, module_progress_schema
from backend.modules.utils import create_module, edit_module, get_module_progress, validate_module
from backend.models import Activity, Module, Student
from backend.prereqs.utils import assign_badge_prereqs
from backend.prereqs.validators import validate_activities, validate_badges

# Blueprint for modules
modules_bp = Blueprint("modules", __name__)


# Class to Read, Update, and Destroy routes
class ModuleData(Resource):
    # Function to return data on a single module
    def get(self, module_id):
        module = Module.query.get(module_id)

        # If module does not exists, then return a 404 error
        # else return the module back to the user
        if not module:
            return {"message": "Module does not exist"}, 404
        else:
            return module_schema.dump(module)

    # Function to edit a module
    def put(self, module_id):
        module = Module.query.get(module_id)

        # If module does not exist, then return a 404 error
        # else edit a module and edit it in the database
        if not module:
            return {"message": "Module does not exist"}, 404
        else:
            form_data = request.get_json()
            errors = module_form_schema.validate(form_data)

            # If form data is not validated by the module_schema, then return a 500 error
            # else edit the module and save it to the database
            if errors:
                return {
                           "message": "Missing or sending incorrect data to edit a module. Double check the JSON data that it has everything needed to edit a module."
                       }, 500
            else:
                activity_error = validate_activities(form_data["activities"])
                badge_error = validate_badges(form_data["badge_prereqs"])

                if activity_error or badge_error:
                    return {
                               "message": "Badge or Activity does not exist. Double check the arrays to check if they are valid in the database."
                           }, 500
                else:
                    edit_module(module, form_data)
                    db.session.commit()

                return {"message": "Module successfully updated"}, 202

    # Function to delete a module
    def delete(self, module_id):
        module = Module.query.get(module_id)

        # If module does not exists, return a 404 error
        # else delete the module and save to database
        if not module:
            return {"message": "Module does not exists"}, 404
        else:
            db.session.delete(module)
            db.session.commit()

        return {"message": "Module successfully deleted"}, 200


# Class to define module creation
class ModuleCreate(Resource):
    # Function to create a module
    def post(self):
        form_data = request.get_json()
        errors = module_form_schema.validate(form_data)
        # If form data is not validated by the module_schema, then return a 500 error
        # else create the module and add it to the database
        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a module. Double check the JSON data that it has everything needed to create a module."
                   }, 500
        else:
            activity_error = validate_activities(form_data["activities"])
            badge_error = validate_badges(form_data["badge_prereqs"])

            if badge_error or activity_error:
                return {
                           "message": "Badge or Activity does not exist. Double check the arrays to check if they are valid in the database."
                       }, 500
            else:
                module = create_module(form_data)
                db.session.add(module)
                db.session.commit()
                assign_badge_prereqs(form_data["badge_prereqs"], module, "Module")
                db.session.commit()

            return {"message": "Module successfully created"}, 202


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
        activity_error = validate_activity(activity_id)

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
api.add_resource(ModuleData, "/modules/<int:module_id>")
api.add_resource(ModuleCreate, "/modules/create")
api.add_resource(ModuleProgress, "/modules/<int:module_id>/progress")

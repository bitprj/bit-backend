from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.modules.schemas import module_schema
from backend.modules.utils import create_module, edit_module
from backend.models import Module


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
            errors = module_schema.validate(form_data)

            # If form data is not validated by the module_schema, then return a 500 error
            # else edit the module and save it to the database
            if errors:
                return {
                            "message": "Missing or sending incorrect data to edit a module. Double check the JSON data that it has everything needed to edit a module."
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
        errors = module_schema.validate(form_data)
        # If form data is not validated by the module_schema, then return a 500 error
        # else create the module and add it to the database
        if errors:
            return {
                "message": "Missing or sending incorrect data to create a module. Double check the JSON data that it has everything needed to create a module."
            }, 500
        else:
            module = create_module(form_data)
            db.session.add(module)
            db.session.commit()

            return {"message": "Module successfully created"}, 202


# Creates the routes for the classes
api.add_resource(ModuleData, "/modules/<int:module_id>")
api.add_resource(ModuleCreate, "/modules/create")

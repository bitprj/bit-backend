from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import auth0_auth
from backend.general_utils import create_schema_json
from backend.models import Module
from backend.modules.decorators import module_exists, module_exists_in_github, valid_module_form
from backend.modules.schemas import module_schema
from backend.modules.utils import create_module, edit_module


# Blueprint for modules
modules_bp = Blueprint("modules", __name__)


# Class for module CRUD routes
class ModuleCRUD(Resource):

    # Function to create a module
    @valid_module_form
    def post(self):
        data = request.get_json()
        module = create_module(data)

        db.session.add(module)
        db.session.commit()
        module.content_url = create_schema_json(module, "module")
        db.session.commit()

        return {"message": "Module successfully created"}, 201

    # Function to edit an module
    @valid_module_form
    @module_exists_in_github
    def put(self):
        data = request.get_json()
        module = Module.query.filter_by(filename=data["filename"]).first()
        edit_module(module, data)

        db.session.commit()

        return {"message": "Module successfully updated"}, 200

    # Function to delete a module!!
    @module_exists_in_github
    def delete(self):
        data = request.get_json()
        module = Module.query.filter_by(filename=data["filename"]).first()

        db.session.delete(module)
        db.session.commit()

        return {"message": "Module successfully deleted"}, 200


# Function to get a specific Module based on module id
class ModuleGetSpecific(Resource):
    method_decorators = [auth0_auth, module_exists]

    def get(self, module_id):
        module = Module.query.get(module_id)

        return module_schema.dump(module)


# Creates the routes for the classes
api.add_resource(ModuleCRUD, "/modules")
api.add_resource(ModuleGetSpecific, "/modules/<int:module_id>")

from flask import (Blueprint, request)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.modules.decorators import module_exists, module_exists_in_contentful
from backend.modules.schemas import module_schema
from backend.modules.utils import create_module, edit_module
from backend.models import Module

# Blueprint for modules
modules_bp = Blueprint("modules", __name__)


# Class for module CRUD routes
class ModuleCRUD(Resource):
    method_decorators = [module_exists_in_contentful]

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
        edit_module(module, contentful_data)

        db.session.commit()

        return {"message": "Module successfully updated"}, 200

    # Function to delete a module!!
    def post(self):
        contentful_data = request.get_json()
        module = Module.query.filter_by(contentful_id=contentful_data["entityId"]).first()

        db.session.delete(module)
        db.session.commit()

        return {"message": "Module successfully deleted"}, 200


# Function to get a specific Module based on module id
class ModuleGetSpecific(Resource):
    method_decorators = [jwt_required, module_exists]

    def get(self, module_id):
        module = Module.query.get(module_id)

        return module_schema.dump(module)


# Creates the routes for the classes
api.add_resource(ModuleCRUD, "/modules")
api.add_resource(ModuleGetSpecific, "/modules/<int:module_id>")

from flask import (Blueprint, request)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.mc_choices.decorators import mc_choice_delete, mc_choice_exists, mc_choice_exists_in_contentful
from backend.mc_choices.schemas import mc_choice_schema
from backend.mc_choices.utils import create_mc_choice, edit_mc_choice
from backend.models import MCChoice

# Blueprint for mc_choices
mc_choices_bp = Blueprint("mc_choices", __name__)


# Class for mc_choice CRUD routes
class MCChoiceCRUD(Resource):
    method_decorators = [mc_choice_exists_in_contentful]

    # Function to create a mc_choice
    def post(self):
        data = request.get_json()
        mc_choice = create_mc_choice(data)

        db.session.add(mc_choice)
        db.session.commit()

        return {"message": "MCChoice successfully created"}, 201

    # Function to edit an mc_choice
    def put(self):
        data = request.get_json()
        mc_choice = MCChoice.query.filter_by(contentful_id=data["entityId"]).first()
        edit_mc_choice(mc_choice, data)

        db.session.commit()

        return {"message": "MCChoice successfully updated"}, 200


# This class is used to delete an mc_choice with a POST request
class MCChoiceDelete(Resource):
    method_decorators = [mc_choice_delete]

    # Function to delete a mc_choice!!
    def post(self):
        data = request.get_json()
        mc_choice = MCChoice.query.filter_by(contentful_id=data["entityId"]).first()

        db.session.delete(mc_choice)
        db.session.commit()

        return {"message": "MCChoice successfully deleted"}, 200


# Function to get a specific MCChoice based on mc_choice id
class MCChoiceGetSpecific(Resource):
    method_decorators = [jwt_required, mc_choice_exists]

    def get(self, mc_choice_id):
        mc_choice = MCChoice.query.get(mc_choice_id)

        return mc_choice_schema.dump(mc_choice)


# Creates the routes for the classes
api.add_resource(MCChoiceCRUD, "/mc_choices")
api.add_resource(MCChoiceDelete, "/mc_choices/delete")
api.add_resource(MCChoiceGetSpecific, "/mc_choices/<int:mc_choice_id>")

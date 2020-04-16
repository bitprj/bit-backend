from backend import api, db
from backend.authentication.decorators import user_session_exists
from backend.mc_choices.decorators import mc_choice_exists, mc_choice_exists_json, mc_choice_exists_in_github, \
    valid_mc_choice_form
from backend.mc_choices.schemas import mc_choice_schema
from backend.mc_choices.utils import create_mc_choice, edit_mc_choice, get_mc_choice
from backend.models import MCChoice
from flask import Blueprint, request
from flask_restful import Resource

# Blueprint for mc_choices
mc_choices_bp = Blueprint("mc_choices", __name__)


# Class for mc_choice CRUD routes
class MCChoiceCRUD(Resource):

    # Function to create a mc_choice
    @valid_mc_choice_form
    def post(self):
        data = request.get_json()
        mc_choice = create_mc_choice(data)

        db.session.add(mc_choice)
        db.session.commit()

        return {"message": "MCChoice successfully created"}, 201

    # Function to edit an mc_choice
    @mc_choice_exists_in_github
    @valid_mc_choice_form
    def put(self):
        data = request.get_json()
        mc_choice = get_mc_choice(data)
        edit_mc_choice(mc_choice, data)

        db.session.commit()

        return {"message": "MCChoice successfully updated"}, 200

    # Function to delete a mc_choice!!
    @mc_choice_exists_in_github
    def delete(self):
        data = request.get_json()
        mc_choice = get_mc_choice(data)

        db.session.delete(mc_choice)
        db.session.commit()

        return {"message": "MCChoice successfully deleted"}, 200


# Function to get a specific MCChoice based on mc_choice id
class MCChoiceGetSpecific(Resource):
    method_decorators = [user_session_exists, mc_choice_exists]

    def get(self, mc_choice_id):
        mc_choice = MCChoice.query.get(mc_choice_id)

        return mc_choice_schema.dump(mc_choice)


# Creates the routes for the classes
api.add_resource(MCChoiceCRUD, "/mc_choices")
api.add_resource(MCChoiceGetSpecific, "/mc_choices/<int:mc_choice_id>")

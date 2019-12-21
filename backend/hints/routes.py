from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.models import Card, Hint
from backend.hints.schemas import hint_schema, hint_form_schema
from backend.hints.utils import create_hint, edit_hint
from backend.steps.utils import validate_step_data

# Blueprint for hints
hints_bp = Blueprint("hints", __name__)


# Class to Read, Update, and Destroy routes
class HintData(Resource):
    # Function to return data on a single hint
    def get(self, hint_id):
        hint = Hint.query.get(hint_id)

        # If hint does not exists, then return a 404 error
        # else return the hint back to the user
        if not hint:
            return {"message": "Hint does not exist"}, 404
        else:
            return hint_schema.dump(hint)

    # Function to edit a hint
    def put(self, hint_id):
        hint = Hint.query.get(hint_id)

        # If hint does not exist, then return a 404 error
        # else edit a hint and edit it in the database
        if not hint:
            return {"message": "Hint does not exist"}, 404
        else:
            form_data = request.get_json()
            errors = hint_form_schema.validate(form_data)
            step_error = validate_step_data(form_data["steps"])

            # If form data is not validated by the hint_schema, then return a 500 error
            # else edit the hint and save it to the database
            if errors or step_error:
                return {
                           "message": "Missing or sending incorrect data to edit a hint. Double check the JSON data that it has everything needed to edit a hint."
                       }, 500
            else:
                edit_hint(hint, form_data)
                db.session.commit()

            return {"message": "Hint successfully updated"}, 202

    # Function to delete a hint
    def delete(self, hint_id):
        hint = Hint.query.get(hint_id)

        # If hint does not exists, return a 404 error
        # else delete the hint and save to database
        if not hint:
            return {"message": "Hint does not exists"}, 404
        else:
            db.session.delete(hint)
            db.session.commit()

        return {"message": "Hint successfully deleted"}, 200


# Class to define hint creation
class HintCreate(Resource):
    # Function to create a hint
    def post(self, card_id):
        form_data = request.get_json()
        errors = hint_form_schema.validate(form_data)
        step_error = validate_step_data(form_data["steps"])

        # If form data is not validated by the hint_schema, then return a 500 error
        # else create the hint and add it to the database
        if errors or step_error:
            return {
                       "message": "Missing or sending incorrect data to create a hint. Double check the JSON data that it has everything needed to create a hint."
                   }, 500
        else:
            card_error = Card.query.get(card_id)

            if not card_error:
                return {
                           "message": "Card or Hint does not exist. Double check the card exists in the database."
                       }, 500
            else:
                hint = create_hint(form_data, card_id)
                db.session.add(hint)
                db.session.commit()

        return {"message": "Hint successfully created"}, 202


# Creates the routes for the classes
api.add_resource(HintData, "/hints/<int:hint_id>")
api.add_resource(HintCreate, "/cards/<int:card_id>/hints/create")

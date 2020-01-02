from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.models import Hint
from backend.hints.schemas import hint_schema
from backend.hints.utils import create_hint, edit_hint

# Blueprint for hints
hints_bp = Blueprint("hints", __name__)


# Class for hint CRUD routes
class HintCRUD(Resource):
    # Function to create a hint
    def post(self):
        contentful_data = request.get_json()
        hint = create_hint(contentful_data)

        db.session.add(hint)
        db.session.commit()

        return {"message": "Hint successfully created"}, 201

    # Function to edit an hint
    def put(self):
        contentful_data = request.get_json()
        hint = Hint.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        edit_hint(hint, contentful_data)

        db.session.commit()

        return {"message": "Hint successfully updated"}, 200


# Function to get a specific Hint based on hint id
class HintGetSpecific(Resource):
    def get(self, hint_id):
        hint = Hint.query.get(hint_id)

        if not hint:
            return {"message": "Hint does not exist"}, 404

        return hint_schema.dump(hint)


# This class is used to delete an hint with a POST request
class HintDelete(Resource):
    # Function to delete a hint!!
    def post(self):
        contentful_data = request.get_json()
        hint = Hint.query.filter_by(contentful_id=contentful_data["entityId"]).first()

        if not hint:
            return {"message": "Hint does not exist"}, 404

        db.session.delete(hint)
        db.session.commit()

        return {"message": "Hint successfully deleted"}, 200


# Creates the routes for the classes
api.add_resource(HintCRUD, "/hints")
api.add_resource(HintGetSpecific, "/hints/<int:hint_id>")
api.add_resource(HintDelete, "/hints/delete")

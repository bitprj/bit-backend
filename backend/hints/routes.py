from flask import (Blueprint, request)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.models import Hint
from backend.hints.decorators import hint_delete, hint_exists, hint_exists_in_contentful
from backend.hints.schemas import hint_schema
from backend.hints.utils import create_hint, delete_hint, edit_hint

# Blueprint for hints
hints_bp = Blueprint("hints", __name__)


# Class for hint CRUD routes
class HintCRUD(Resource):
    method_decorators = [hint_exists_in_contentful]

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


# This class is used to delete an hint with a POST request
class HintDelete(Resource):
    method_decorators = [hint_delete]

    # Function to delete a hint!!
    def post(self):
        contentful_data = request.get_json()
        hint = Hint.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        delete_hint(hint)

        db.session.delete(hint)
        db.session.commit()

        return {"message": "Hint successfully deleted"}, 200


# Function to get a specific Hint based on hint id
class HintGetSpecific(Resource):
    method_decorators = [jwt_required, hint_exists]

    def get(self, hint_id):
        hint = Hint.query.get(hint_id)

        return hint_schema.dump(hint)


# Creates the routes for the classes
api.add_resource(HintCRUD, "/hints")
api.add_resource(HintGetSpecific, "/hints/<int:hint_id>")
api.add_resource(HintDelete, "/hints/delete")

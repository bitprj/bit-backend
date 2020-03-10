from flask import (Blueprint, request)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.config import API
from backend.models import Hint
from backend.hints.decorators import hint_exists, hint_exists_in_github, valid_hint_form
from backend.hints.schemas import hint_schema
from backend.hints.utils import assign_hint_to_parent, create_hint, edit_hint
import requests

# Blueprint for hints
hints_bp = Blueprint("hints", __name__)


# Class for hint CRUD routes
class HintCRUD(Resource):

    # Function to create a hint
    @valid_hint_form
    def post(self):
        data = request.get_json()
        hint = create_hint(data)

        db.session.add(hint)
        db.session.commit()
        assign_hint_to_parent(hint, data)
        # data = {"github_raw_data": data["github_raw_data"], "hint_id": hint.id}
        # requests.post(API + "/steps", json=data)

        db.session.commit()

        return {"message": "Hint successfully created"}, 201

    # Function to edit an hint
    @valid_hint_form
    @hint_exists_in_github
    def put(self):
        data = request.get_json()
        hint = Hint.query.filter_by(github_raw_data=data["github_raw_data"]).first()
        edit_hint(hint, data)
        # data = {"github_raw_data": data["github_raw_data"], "hint_id": hint.id}
        # requests.put(API + "/steps", json=data)

        db.session.commit()

        return {"message": "Hint successfully updated"}, 200

    # Function to delete a hint!!
    @hint_exists_in_github
    def delete(self):
        data = request.get_json()
        hint = Hint.query.filter_by(filename=data["filename"]).first()

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

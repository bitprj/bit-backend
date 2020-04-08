from flask import (Blueprint, request)
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from backend import api, db
from backend.general_utils import create_schema_json
from backend.models import ActivityProgress, Hint, HintStatus, Student
from backend.hints.decorators import hint_exists, hint_exists_in_github, valid_hint_form
from backend.hints.schemas import hint_schema, hint_status_schema
from backend.hints.utils import assign_hint_to_parent, create_hint, edit_hint, get_activity_id
from backend.hooks.utils import call_step_routes

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
        call_step_routes(data, hint.id, "hint")
        create_schema_json(hint, "hints")
        db.session.commit()

        return {"message": "Hint successfully created"}, 201

    # Function to edit an hint
    @valid_hint_form
    @hint_exists_in_github
    def put(self):
        data = request.get_json()
        hint = Hint.query.filter_by(filename=data["filename"]).first()
        edit_hint(hint, data)

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


# Function to handle data on HintStatus
class HintStatusData(Resource):
    method_decorators = [jwt_required, hint_exists]

    def get(self, hint_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        hint = Hint.query.get(hint_id)
        activity_id = get_activity_id(hint)
        activity_prog = ActivityProgress.query.filter_by(student_id=student.id,
                                                         activity_id=activity_id).first()
        hint_status = HintStatus.query.filter_by(activity_progress_id=activity_prog.id, hint_id=hint_id).first()

        return hint_status_schema.dump(hint_status)


# Creates the routes for the classes
api.add_resource(HintCRUD, "/hints")
api.add_resource(HintGetSpecific, "/hints/<int:hint_id>")
api.add_resource(HintStatusData, "/hints/<int:hint_id>/progress")

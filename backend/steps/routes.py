from flask import (Blueprint, request)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.hooks.utils import md_to_json
from backend.models import Step
from backend.steps.decorators import step_exists, step_exists_in_github, valid_step_form
from backend.steps.schemas import step_schema
from backend.steps.utils import create_step, edit_step

# Blueprint for steps
steps_bp = Blueprint("steps", __name__)


# Class for step CRUD routes
class StepCRUD(Resource):

    # Function to create a step
    # @valid_step_form
    def post(self):
        data = request.get_json()
        content_data = md_to_json(data["github_raw_data"])
        image_folder = content_data.pop("image_folder")

        for step_key, step_data in content_data.items():
            step = create_step(step_key, step_data, data["hint_id"], image_folder)
            db.session.add(step)

        db.session.commit()

        return {"message": "Step successfully created"}, 201

    # Function to edit an step
    # @valid_step_form
    # @step_exists_in_github
    def put(self):
        data = request.get_json()
        content_data = md_to_json(data["github_raw_data"])
        image_folder = content_data.pop("image_folder")

        for step_key, step_data in content_data.items():
            step = Step.query.filter_by(hint_id=data["hint_id"], step_key=step_key).first()

            if step:
                edit_step(step, step_data, image_folder)
            else:
                step = create_step(step_key, step_data, data["hint_id"], image_folder)
                db.session.add(step)

        db.session.commit()

        return {"message": "Step successfully updated"}, 200

    # Function to delete a step!!
    @step_exists_in_github
    def delete(self):
        data = request.get_json()
        step = Step.query.filter_by(hint_id=data["hint_id"]).first()

        db.session.delete(step)
        db.session.commit()

        return {"message": "Step successfully deleted"}, 200


# Function to get a specific Step based on step id
class StepGetSpecific(Resource):
    method_decorators = [jwt_required, step_exists]

    def get(self, step_id):
        step = Step.query.get(step_id)

        return step_schema.dump(step)


# Creates the routes for the classes
api.add_resource(StepCRUD, "/steps")
api.add_resource(StepGetSpecific, "/steps/<int:step_id>")

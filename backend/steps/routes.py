from backend import api, db
from backend.authentication.decorators import user_session_exists
from backend.models import Step
from backend.steps.decorators import step_exists, step_exists_in_github, valid_step_form
from backend.steps.schemas import step_schema
from backend.steps.utils import create_step, edit_step, generate_step_cdn_url, get_step_from_patent
from flask import Blueprint, request
from flask_restful import Resource

# Blueprint for steps
steps_bp = Blueprint("steps", __name__)


# Class for step CRUD routes
class StepCRUD(Resource):

    # Function to create a step
    @valid_step_form
    def post(self):
        data = request.get_json()
        step = create_step(data)

        db.session.add(step)
        db.session.commit()
        generate_step_cdn_url(step)
        db.session.commit()

        return {"message": "Step successfully created"}, 201

    # Function to edit an step
    @valid_step_form
    @step_exists_in_github
    def put(self):
        data = request.get_json()
        step = get_step_from_patent(data)
        edit_step(step, data)

        db.session.commit()

        return {"message": "Step successfully updated"}, 200

    # Function to delete a step!!
    @step_exists_in_github
    def delete(self):
        data = request.get_json()
        step = get_step_from_patent(data)

        db.session.delete(step)
        db.session.commit()

        return {"message": "Step successfully deleted"}, 200


# Function to get a specific Step based on step id
class StepGetSpecific(Resource):
    method_decorators = [user_session_exists, step_exists]

    def get(self, step_id):
        step = Step.query.get(step_id)

        return step_schema.dump(step)


# Creates the routes for the classes
api.add_resource(StepCRUD, "/steps")
api.add_resource(StepGetSpecific, "/steps/<int:step_id>")

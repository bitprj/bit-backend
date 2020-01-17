from flask import (Blueprint, request)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.models import Step
from backend.steps.decorators import step_delete, step_exists, step_exists_in_contentful
from backend.steps.schemas import step_schema
from backend.steps.utils import create_step, edit_step

# Blueprint for steps
steps_bp = Blueprint("steps", __name__)


# Class for step CRUD routes
class StepCRUD(Resource):
    method_decorators = [step_exists_in_contentful]

    # Function to create a step
    def post(self):
        contentful_data = request.get_json()
        step = create_step(contentful_data)

        db.session.add(step)
        db.session.commit()

        return {"message": "Step successfully created"}, 201

    # Function to edit an step
    def put(self):
        contentful_data = request.get_json()
        step = Step.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        edit_step(step, contentful_data)

        db.session.commit()

        return {"message": "Step successfully updated"}, 200


# This class is used to delete an step with a POST request
class StepDelete(Resource):
    method_decorators = [step_delete]

    # Function to delete a step!!
    def post(self):
        contentful_data = request.get_json()
        print(contentful_data)
        step = Step.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        print(step)
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
api.add_resource(StepDelete, "/steps/delete")

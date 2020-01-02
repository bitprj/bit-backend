from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.models import Step
from backend.steps.schemas import step_schema
from backend.steps.utils import create_step, edit_step

# Blueprint for steps
steps_bp = Blueprint("steps", __name__)


# Class for step CRUD routes
class StepCRUD(Resource):
    # Function to create a step
    def post(self):
        contentful_data = request.get_json()
        print(contentful_data)
        step = create_step(contentful_data)

        db.session.add(step)
        db.session.commit()
        print(step.id)
        return {"message": "Step successfully created"}, 201

    # Function to edit an step
    def put(self):
        contentful_data = request.get_json()
        print(contentful_data)
        step = Step.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        edit_step(step, contentful_data)

        db.session.commit()
        print(step.id)

        return {"message": "Step successfully updated"}, 200


# Function to get a specific Step based on step id
class StepGetSpecific(Resource):
    def get(self, step_id):
        step = Step.query.get(step_id)

        if not step:
            return {"message": "Step does not exist"}, 404
        print(step.id)

        return step_schema.dump(step)


# This class is used to delete an step with a POST request
class StepDelete(Resource):
    # Function to delete a step!!
    def post(self):
        contentful_data = request.get_json()
        print(contentful_data)
        step = Step.query.filter_by(contentful_id=contentful_data["entityId"]).first()

        if not step:
            return {"message": "Step does not exist"}, 404
        print(step.id)

        db.session.delete(step)
        db.session.commit()

        return {"message": "Step successfully deleted"}, 200


# Creates the routes for the classes
api.add_resource(StepCRUD, "/steps")
api.add_resource(StepGetSpecific, "/steps/<int:step_id>")
api.add_resource(StepDelete, "/steps/delete")

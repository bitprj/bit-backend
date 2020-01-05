from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.checkpoints.schemas import checkpoint_schema
from backend.checkpoints.utils import create_checkpoint, edit_checkpoint
from backend.models import Checkpoint

# Blueprint for checkpoints
checkpoints_bp = Blueprint("checkpoints", __name__)


# Class to Read, Create, and Update
class CheckpointCRUD(Resource):
    # Function to create a checkpoint or edit a checkpoint
    def post(self):
        contentful_data = request.get_json()
        print(contentful_data)

        checkpoint = Checkpoint.query.filter_by(contentful_id=contentful_data["entityId"]).first()

        if not checkpoint:
            print("creating")
            edit_checkpoint(checkpoint, contentful_data)
            db.session.commit()
            print(checkpoint.id)
            return {"message": "Checkpoint successfully created"}, 201
        else:
            print("editing")
            checkpoint = create_checkpoint(contentful_data)
            db.session.add(checkpoint)
            db.session.commit()
            print(checkpoint.id)

            return {"message": "Checkpoint successfully updated"}, 200


# This class is used to delete a checkpoint with a POST request
class CheckpointDelete(Resource):
    # Function to delete a checkpoint
    def post(self):
        contentful_data = request.get_json()
        print(contentful_data)
        checkpoint = Checkpoint.query.filter_by(contentful_id=contentful_data["entityId"]).first()

        if not checkpoint:
            return {"message": "Checkpoint does not exist"}, 404
        print(checkpoint.id)

        db.session.delete(checkpoint)
        db.session.commit()

        return {"message": "Checkpoint successfully deleted"}, 200


# This class is used to get a specific checkpoint based on id
class CheckpointGetSpecific(Resource):
    # Function to return data on a single checkpoint
    def get(self, checkpoint_id):
        checkpoint = Checkpoint.query.get(checkpoint_id)

        # If checkpoint does not exists, then return a 404 error
        # else return the checkpoint back to the user
        if not checkpoint:
            return {"message": "Checkpoint does not exist"}, 404
        else:
            return checkpoint_schema.dump(checkpoint)


# Creates the routes for the classes
api.add_resource(CheckpointCRUD, "/checkpoints")
api.add_resource(CheckpointDelete, "/checkpoints/delete")
api.add_resource(CheckpointGetSpecific, "/checkpoints/<int:checkpoint_id>")

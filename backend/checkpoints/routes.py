from backend import api, db
from backend.authentication.decorators import user_session_exists
from backend.checkpoints.decorators import checkpoint_exists, checkpoint_exists_in_github, valid_checkpoint_form, \
    valid_checkpoint_type
from backend.checkpoints.schemas import checkpoint_schema
from backend.checkpoints.utils import assign_checkpoint_to_card, create_checkpoint, edit_checkpoint, \
    fill_optional_checkpoint_fields
from backend.general_utils import create_schema_json
from backend.models import Card, Checkpoint
from flask import Blueprint, request
from flask_restful import Resource


# Blueprint for checkpoints
checkpoints_bp = Blueprint("checkpoints", __name__)


# Class to Read, Create, and Update
class CheckpointCRUD(Resource):

    # Function to create a checkpoint
    @valid_checkpoint_form
    @valid_checkpoint_type
    def post(self):
        data = request.get_json()
        checkpoint = create_checkpoint(data)

        db.session.add(checkpoint)
        db.session.commit()
        assign_checkpoint_to_card(checkpoint, data)
        fill_optional_checkpoint_fields(checkpoint, data)
        create_schema_json(checkpoint, "checkpoints")
        card = Card.query.filter_by(checkpoint_id=checkpoint.id).first()
        create_schema_json(card, "cards")
        db.session.commit()

        return {"message": "Checkpoint successfully created"}, 201

    # Function to edit a checkpoint
    @checkpoint_exists_in_github
    @valid_checkpoint_form
    @valid_checkpoint_type
    def put(self):
        data = request.get_json()
        checkpoint = Checkpoint.query.filter_by(filename=data["filename"]).first()
        edit_checkpoint(checkpoint, data)

        db.session.commit()

        return {"message": "Checkpoint successfully updated"}, 200

    # Function to delete a checkpoint
    @checkpoint_exists_in_github
    def delete(self):
        data = request.get_json()
        checkpoint = Checkpoint.query.filter_by(filename=data["filename"]).first()

        db.session.delete(checkpoint)
        db.session.commit()

        return {"message": "Checkpoint successfully deleted"}, 200


# This class is used to get a specific checkpoint based on id
class CheckpointGetSpecific(Resource):
    method_decorators = [user_session_exists, checkpoint_exists]

    # Function to return data on a single checkpoint
    def get(self, checkpoint_id):
        checkpoint = Checkpoint.query.get(checkpoint_id)

        return checkpoint_schema.dump(checkpoint)


# Creates the routes for the classes
api.add_resource(CheckpointCRUD, "/checkpoints")
api.add_resource(CheckpointGetSpecific, "/checkpoints/<int:checkpoint_id>")

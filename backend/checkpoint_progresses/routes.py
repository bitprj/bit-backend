from flask import (Blueprint, request)
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api, db
from backend.general_utils import add_image, get_user_id_from_token
from backend.models import Checkpoint, CheckpointProgress

# Blueprint for checkpoints
checkpoint_progresses_bp = Blueprint("checkpoint_progresses", __name__)


# This class is used to get a specific checkpoint based on id
class CheckpointProgressSubmit(Resource):
    method_decorators = [roles_accepted("Student")]

    # Function to return data on a single checkpoint
    def put(self, checkpoint_id):
        current_user_id = get_user_id_from_token()
        image_file = request.files["image"]
        checkpoint_prog = CheckpointProgress.query.filter_by(checkpoint_id=checkpoint_id,
                                                             student_id=current_user_id).first()
        if checkpoint_prog:
            checkpoint = Checkpoint.query.get(checkpoint_id)

            if checkpoint.checkpoint_type == "Image":
                image = add_image(image_file, "checkpoints")
                checkpoint_prog.image_to_receive = image
            elif checkpoint.checkpoint_type == "okPy":
                print("data to receive from john's code")

            checkpoint_prog.is_completed = True
            db.session.commit()
        else:
            return {
                       "message": "Checkpoint does not exist or you do not own this checkpoint"
                   }, 500

        return {
                   "message": "Checkpoint Progress recorded"
               }, 200


# Creates the routes for the classes
api.add_resource(CheckpointProgressSubmit, "/checkpoints/<int:checkpoint_id>/submit")

from flask import (Blueprint, request)
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api, db
from backend.activity_progresses.utils import is_activity_completed
from backend.general_utils import add_file, get_user_id_from_token, get_user_id
from backend.models import Checkpoint, CheckpointProgress

# Blueprint for checkpoints
checkpoint_progresses_bp = Blueprint("checkpoint_progresses", __name__)


# This class is used to get a specific checkpoint based on id
class CheckpointProgressSubmit(Resource):
    method_decorators = [roles_accepted("Student")]

    # Function to return data on a single checkpoint
    def put(self, checkpoint_id):
        checkpoint = Checkpoint.query.get(checkpoint_id)
        checkpoint_prog = None

        if checkpoint.checkpoint_type == "okPy":
            current_user_id = get_user_id(request.form)
            checkpoint_prog = CheckpointProgress.query.filter_by(checkpoint_id=checkpoint_id,
                                                                 student_id=current_user_id).first()
        else:
            current_user_id = get_user_id_from_token()
            checkpoint_prog = CheckpointProgress.query.filter_by(checkpoint_id=checkpoint_id,
                                                                 student_id=current_user_id).first()
        if checkpoint_prog:
            if checkpoint.checkpoint_type == "Image":
                image_file = request.files["image"]
                image = add_file(image_file, "checkpoints")
                checkpoint_prog.image_to_receive = image
            elif checkpoint.checkpoint_type == "Video":
                video_file = request.files["video"]
                video = add_file(video_file, "checkpoints")
                checkpoint_prog.video_to_receive = video
            elif checkpoint.checkpoint_type == "okPy":
                print(request.form)
                print("data to receive from john's code")

            checkpoint_prog.is_completed = True
            db.session.commit()
            is_activity_completed(checkpoint_prog.activity_progress_id, student_id=checkpoint_prog.student_id)
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

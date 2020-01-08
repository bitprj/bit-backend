from flask import (Blueprint, request)
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api, db
from backend.activity_progresses.utils import is_activity_completed
from backend.checkpoint_progresses.utils import fill_in_checkpoint_progress
from backend.general_utils import get_user_id_from_token, get_user_id
from backend.models import Checkpoint, CheckpointProgress
import ast

# Blueprint for checkpoints
checkpoint_progresses_bp = Blueprint("checkpoint_progresses", __name__)


# This class is used to get a specific checkpoint based on id
class CheckpointProgressSubmit(Resource):
    # method_decorators = [roles_accepted("Student")]

    # Function to return data on a single checkpoint
    def put(self, checkpoint_id):
        data = request.get_json()
        checkpoint = Checkpoint.query.get(checkpoint_id)

        if checkpoint.checkpoint_type == "okPy":
            current_user_id = get_user_id(data["jwt_token"])
        else:
            current_user_id = get_user_id_from_token()

        checkpoint_prog = CheckpointProgress.query.filter_by(checkpoint_id=checkpoint_id,
                                                             student_id=current_user_id).first()

        if checkpoint_prog:
            fill_in_checkpoint_progress(data, checkpoint_prog)
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

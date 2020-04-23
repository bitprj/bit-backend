from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.checkpoints.decorators import checkpoint_exists
from backend.checkpoint_progresses.decorators import checkpoint_progress_exist, multiple_choice_is_completed, \
    valid_checkpoint_progress_data
from backend.activity_progresses.utils import is_activity_completed
from backend.authentication.decorators import user_session_exists
from backend.checkpoint_progresses.utils import fill_in_checkpoint_progress, get_checkpoint_data
from backend.models import CheckpointProgress
from flask import Blueprint, request, session
from flask_restful import Resource

# Blueprint for checkpoints
checkpoint_progresses_bp = Blueprint("checkpoint_progresses", __name__)


# This class is used to get a specific checkpoint based on id
class CheckpointProgressSubmit(Resource):
    method_decorators = [user_session_exists, roles_accepted("Student"), checkpoint_exists]

    # Function to retrieve data from a checkpoint progress
    @checkpoint_progress_exist
    def get(self, checkpoint_id):
        user_data = session["profile"]
        checkpoint_prog = CheckpointProgress.query.filter_by(checkpoint_id=checkpoint_id,
                                                             student_id=user_data["student_id"]).first()

        return get_checkpoint_data(checkpoint_prog)

    # Function to return data on a single checkpoint
    @checkpoint_progress_exist
    @valid_checkpoint_progress_data
    @multiple_choice_is_completed
    def put(self, checkpoint_id):
        data = request.form
        user_data = session["profile"]
        checkpoint_prog = CheckpointProgress.query.filter_by(checkpoint_id=checkpoint_id,
                                                             student_id=user_data["student_id"]).first()
        fill_in_checkpoint_progress(data, checkpoint_prog)
        db.session.commit()
        is_activity_completed(checkpoint_prog.activity_progress_id, checkpoint_prog.student_id)
        db.session.commit()

        return get_checkpoint_data(checkpoint_prog)


# Creates the routes for the classes
api.add_resource(CheckpointProgressSubmit, "/checkpoints/<int:checkpoint_id>/progress")

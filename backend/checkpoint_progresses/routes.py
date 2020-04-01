from flask import (Blueprint, request)
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.checkpoints.decorators import checkpoint_exists
from backend.checkpoint_progresses.decorators import checkpoint_progress_exist, multiple_choice_is_completed, \
    valid_checkpoint_progress_data
from backend.activity_progresses.utils import is_activity_completed
from backend.checkpoint_progresses.utils import fill_in_checkpoint_progress, get_checkpoint_data
from backend.models import CheckpointProgress, Student

# Blueprint for checkpoints
checkpoint_progresses_bp = Blueprint("checkpoint_progresses", __name__)


# This class is used to get a specific checkpoint based on id
class CheckpointProgressSubmit(Resource):
    method_decorators = [roles_accepted("Student"), checkpoint_exists]

    # Function to retrieve data from a checkpoint progress
    @checkpoint_progress_exist
    def get(self, checkpoint_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        checkpoint_prog = CheckpointProgress.query.filter_by(checkpoint_id=checkpoint_id,
                                                             student_id=student.id).first()

        return get_checkpoint_data(checkpoint_prog)

    # Function to return data on a single checkpoint
    @checkpoint_progress_exist
    @valid_checkpoint_progress_data
    @multiple_choice_is_completed
    def put(self, checkpoint_id):
        data = request.form
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        checkpoint_prog = CheckpointProgress.query.filter_by(checkpoint_id=checkpoint_id,
                                                             student_id=student.id).first()
        fill_in_checkpoint_progress(data, checkpoint_prog)

        db.session.commit()
        is_activity_completed(checkpoint_prog.activity_progress_id, student_id=checkpoint_prog.student_id)
        db.session.commit()

        return get_checkpoint_data(checkpoint_prog)


# Creates the routes for the classes
api.add_resource(CheckpointProgressSubmit, "/checkpoints/<int:checkpoint_id>/progress")

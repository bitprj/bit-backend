from flask import (Blueprint, request)
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.checkpoints.decorators import checkpoint_exists
from backend.activity_progresses.utils import is_activity_completed
from backend.checkpoint_progresses.utils import fill_in_checkpoint_progress
from backend.models import CheckpointProgress, Student

# Blueprint for checkpoints
checkpoint_progresses_bp = Blueprint("checkpoint_progresses", __name__)


# This class is used to get a specific checkpoint based on id
class CheckpointProgressSubmit(Resource):
    method_decorators = [roles_accepted("Student"), checkpoint_exists]

    # Function to return data on a single checkpoint
    def put(self, checkpoint_id):
        data = request.get_json()
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        checkpoint_prog = CheckpointProgress.query.filter_by(checkpoint_id=checkpoint_id,
                                                             student_id=student.id).first()
        print(checkpoint_prog.checkpoint.checkpoint_type)
        if checkpoint_prog:
            fill_in_checkpoint_progress(data, checkpoint_prog)
            checkpoint_prog.is_completed = True
            print(checkpoint_prog.short_answer_response)
            # db.session.commit()
            # is_activity_completed(checkpoint_prog.activity_progress_id, student_id=checkpoint_prog.student_id)
            # db.session.commit()
        else:
            return {
                       "message": "Checkpoint does not exist or you do not own this checkpoint"
                   }, 500

        return {
                   "message": "Checkpoint Progress recorded"
               }, 200


# Creates the routes for the classes
api.add_resource(CheckpointProgressSubmit, "/checkpoints/<int:checkpoint_id>/submit")

from flask import (Blueprint)
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.models import Student, Topic
from backend.topics.decorators import can_add_topic, can_complete_topic, has_completed_topic, topic_exists
from backend.tracks.decorators import *
from backend.tracks.schemas import track_progress_schema
from backend.tracks.utils import get_track_progress

# Blueprint for track progresses
track_progresses_bp = Blueprint("track_progresses", __name__)


# Class to handle track progress
class TrackProgress(Resource):
    method_decorators = [track_exists, roles_accepted("Student")]

    # Function to retrieve the students track progress
    def get(self, track_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()

        track_progress = get_track_progress(student.id, track_id)
        return track_progress_schema.dump(track_progress)


# Class to handle adding a topic track progress
class TrackProgressAdd(Resource):
    method_decorators = [roles_accepted("Student"), topic_exists]

    # Function to add a topic to a student's inprogress_topics
    @can_add_topic
    def put(self, topic_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        topic = Topic.query.get(topic_id)
        student.inprogress_topics.append(topic)

        if topic in student.incomplete_topics:
            student.inprogress_topics.remove(topic)

        db.session.commit()

        return {
                   "message": "Topic added!"
               }, 201


# Class to update a track progress
class TrackProgressUpdate(Resource):
    method_decorators = [roles_accepted("Student"), topic_exists]

    # Function to update the student's completed topic
    @can_complete_topic
    @has_completed_topic
    def put(self, topic_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        topic = Topic.query.get(topic_id)
        student.completed_topics.append(topic)
        student.inprogress_topics.remove(topic)

        db.session.commit()

        return {"message": "Student topic successfully updated!"}


api.add_resource(TrackProgress, "/tracks/<int:track_id>/progress")
api.add_resource(TrackProgressAdd, "/tracks/progress/<int:topic_id>/add_topic")
api.add_resource(TrackProgressUpdate, "/tracks/progress/<int:topic_id>")

from flask import (Blueprint)
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api, db
from backend.general_utils import get_user_id_from_token
from backend.models import Student, Topic
from backend.topics.decorators import topic_exists, can_add_topic, can_complete_topic
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
        current_user_id = get_user_id_from_token()

        track_progress = get_track_progress(current_user_id, track_id)
        return track_progress_schema.dump(track_progress)


# Class to handle adding a topic track progress
class TrackProgressAdd(Resource):
    method_decorators = [roles_accepted("Student"), topic_exists, can_add_topic]

    # Function to add a topic to a student's inprogress_topics
    def put(self, topic_id):
        current_user_id = get_user_id_from_token()
        student = Student.query.get(current_user_id)
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
    method_decorators = [roles_accepted("Student"), topic_exists, can_complete_topic]

    # Function to update the student's completed topic
    def put(self, topic_id):
        current_user_id = get_user_id_from_token()
        student = Student.query.get(current_user_id)
        topic = Topic.query.get(topic_id)
        student.completed_topics.append(topic)
        student.inprogress_topics.remove(topic)

        db.session.commit()

        return {"message": "Student topic successfully updated!"}


api.add_resource(TrackProgress, "/tracks/<int:track_id>/progress")
api.add_resource(TrackProgressAdd, "/tracks/progress/<int:topic_id>/add_topic")
api.add_resource(TrackProgressUpdate, "/tracks/progress/<int:topic_id>")

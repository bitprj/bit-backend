from flask import (Blueprint, request)
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api, db
from backend.general_utils import get_user_id_from_token
from backend.tracks.schemas import track_schema, tracks_schema, track_progress_schema
from backend.tracks.utils import create_track, edit_track, get_track_progress, validate_track
from backend.models import Student, Track

# Blueprint for tracks
tracks_bp = Blueprint("tracks", __name__)


# Class for track CRUD routes
class TrackCRUD(Resource):
    # Function to get all tracks
    def get(self):
        tracks = Track.query.all()

        return tracks_schema.dump(tracks)

    # Function to create a track
    def post(self):
        contentful_data = request.get_json()
        track = create_track(contentful_data)

        db.session.add(track)
        db.session.commit()

        return {"message": "Track successfully created"}, 201

    # Function to edit an track
    def put(self):
        contentful_data = request.get_json()
        track = Track.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        edit_track(track, contentful_data)

        db.session.commit()

        return {"message": "Track successfully updated"}, 200


# Function to get a specific Track based on track id
class TrackGetSpecific(Resource):
    def get(self, track_id):
        track = Track.query.get(track_id)

        if not track:
            return {"message": "Track does not exist"}, 404

        return track_schema.dump(track)


# This class is used to delete an track with a POST request
class TrackDelete(Resource):
    # Function to delete a track!!
    def post(self):
        contentful_data = request.get_json()
        track = Track.query.filter_by(contentful_id=contentful_data["entityId"]).first()

        db.session.delete(track)
        db.session.commit()

        return {"message": "Track successfully deleted"}, 200


# Class to handle track progress
class TrackProgress(Resource):
    method_decorators = [roles_accepted("Student")]

    # Function to retrieve the students track progress
    def get(self, track_id):
        current_user_id = get_user_id_from_token()
        track_error = validate_track(track_id)

        if track_error:
            return {
                       "message": "Track does not exist."
                   }, 500
        else:
            track_progress = get_track_progress(current_user_id, track_id)
            return track_progress_schema.dump(track_progress)

    # Function to update the student's completed topic
    def put(self, track_id):
        current_user_id = get_user_id_from_token()
        student = Student.query.get(current_user_id)
        topic_completed = request.get_json()
        topic_id = topic_completed["complete"]["id"]
        track_error = validate_track(track_id)

        if track_error:
            return {
                       "message": "Track does not exist."
                   }, 500
        else:
            # if the sent topic_id does not match the student's current topic id then send an error
            if student.current_topic_id != topic_id:
                return {
                           "message": "Sent topic id does not match the student's current topic_id."
                       }, 500
            else:
                student.completed_topics.append(student.topic)
                student.current_topic_id = None
                db.session.commit()

        return {"message": "Student topic successfully updated!"}


# Creates the routes for the classes
api.add_resource(TrackCRUD, "/tracks")
api.add_resource(TrackDelete, "/tracks/delete")
api.add_resource(TrackGetSpecific, "/tracks/<int:track_id>")
api.add_resource(TrackProgress, "/tracks/<int:track_id>/progress")

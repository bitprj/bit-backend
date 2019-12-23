from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.general_utils import get_user_id_from_token
from backend.models import Student, Track
from backend.prereqs.validators import validate_topics
from backend.tracks.schemas import track_schema, track_form_schema, track_progress_schema
from backend.tracks.utils import create_track, edit_track, validate_track
from flask_praetorian.decorators import roles_accepted

# Blueprint for tracks
tracks_bp = Blueprint("tracks", __name__)


# Class to Read, Update, and Destroy routes
class TrackData(Resource):
    # Function to return data on a single track
    def get(self, track_id):
        track = Track.query.get(track_id)

        # If track does not exists, then return a 404 error
        # else return the track back to the user
        if not track:
            return {"message": "Track does not exist"}, 404
        else:
            return track_schema.dump(track)

    # Function to edit a track
    def put(self, track_id):
        track = Track.query.get(track_id)

        # If track does not exist, then return a 404 error
        # else edit a track and edit it in the database
        if not track:
            return {"message": "Track does not exist"}, 404
        else:
            form_data = request.get_json()
            errors = track_form_schema.validate(form_data)

            # If form data is not validated by the track_schema, then return a 500 error
            # else edit the track and save it to the database
            if errors:
                return {
                           "message": "Missing or sending incorrect data to edit a track. Double check the JSON data that it has everything needed to edit a track."
                       }, 500
            else:
                track_error = validate_topics(form_data["topics"])
                required_track_error = validate_topics(form_data["required_topics"])

                if track_error or required_track_error:
                    return {
                               "message": "Topic does not exist. Double check the arrays to check if they are valid in the database."
                           }, 500
                else:
                    edit_track(track, form_data)
                    db.session.commit()

                return {"message": "Track successfully updated"}, 202

    # Function to delete a track
    def delete(self, track_id):
        track = Track.query.get(track_id)

        # If track does not exists, return a 404 error
        # else delete the track and save to database
        if not track:
            return {"message": "Track does not exists"}, 404
        else:
            db.session.delete(track)
            db.session.commit()

        return {"message": "Track successfully deleted"}, 200


# Class to define track creation
class TrackCreate(Resource):
    # Function to create a track
    def post(self):
        form_data = request.get_json()
        errors = track_form_schema.validate(form_data)

        # If form data is not validated by the track_schema, then return a 500 error
        # else create the track and add it to the database
        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a track. Double check the JSON data that it has everything needed to create a track."
                   }, 500
        else:
            track_error = validate_topics(form_data["topics"])
            required_track_error = validate_topics(form_data["required_topics"])

            if track_error or required_track_error:
                return {
                           "message": "Topic does not exist. Double check the arrays to check if they are valid in the database."
                       }, 500
            else:
                track = create_track(form_data)
                db.session.add(track)
                db.session.commit()

            return {"message": "Track successfully created"}, 202


# Class to handle track progress
class TrackProgress(Resource):
    method_decorators = [roles_accepted("Student")]
    
    # Function to retrieve the students track progress
    def get(self, track_id):
        current_user_id = get_user_id_from_token()
        student = Student.query.get(current_user_id)
        track_error = validate_track(track_id)

        if track_error:
            return {
                       "message": "Track does not exist."
                   }, 500
        else:
            return track_progress_schema.dump(student)

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
api.add_resource(TrackData, "/tracks/<int:track_id>")
api.add_resource(TrackCreate, "/tracks/create")
api.add_resource(TrackProgress, "/tracks/<int:track_id>/progress")

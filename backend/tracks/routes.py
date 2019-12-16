from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.tracks.schemas import track_schema
from backend.tracks.utils import create_track, edit_track
from backend.models import Track


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
            errors = track_schema.validate(form_data)

            # If form data is not validated by the track_schema, then return a 500 error
            # else edit the track and save it to the database
            if errors:
                return {
                            "message": "Missing or sending incorrect data to edit a track. Double check the JSON data that it has everything needed to edit a track."
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
        errors = track_schema.validate(form_data)
        # If form data is not validated by the track_schema, then return a 500 error
        # else create the track and add it to the database
        if errors:
            return {
                "message": "Missing or sending incorrect data to create a track. Double check the JSON data that it has everything needed to create a track."
            }, 500
        else:
            track = create_track(form_data)
            db.session.add(track)
            db.session.commit()

            return {"message": "Track successfully created"}, 202


# Creates the routes for the classes
api.add_resource(TrackData, "/tracks/<int:track_id>")
api.add_resource(TrackCreate, "/tracks/create")

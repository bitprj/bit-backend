from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.general_utils import send_file_to_cdn
from backend.models import Track
from backend.tracks.decorators import track_exists, track_exists_in_github, valid_track_form
from backend.tracks.schemas import track_schema, tracks_schema
from backend.tracks.utils import create_track, edit_track

# Blueprint for tracks
tracks_bp = Blueprint("tracks", __name__)


# Class for track CRUD routes
class TrackCRUD(Resource):
    # Function to create a track
    @valid_track_form
    def post(self):
        data = request.get_json()
        track = create_track(data)

        db.session.add(track)
        db.session.commit()
        track_data = track_schema.dump(track)
        track.content_url = send_file_to_cdn(track_data, track.filename, "tracks", track)
        db.session.commit()

        return {"message": "Track successfully created"}, 201

    # Function to edit an track
    @track_exists_in_github
    @valid_track_form
    def put(self):
        data = request.get_json()
        track = Track.query.filter_by(github_id=data["github_id"]).first()
        edit_track(data, track)

        db.session.commit()

        return {"message": "Track successfully updated"}, 200

    # Function to delete a track!!
    @track_exists_in_github
    def delete(self):
        data = request.get_json()
        track = Track.query.filter_by(github_id=data["github_id"]).first()

        db.session.delete(track)
        db.session.commit()

        return {"message": "Track successfully deleted"}, 200


# Class to get all tracks
class TrackFetchAll(Resource):
    method_decorators = [jwt_required]

    # Function to get all tracks
    def get(self):
        tracks = Track.query.all()

        return tracks_schema.dump(tracks)


# Function to get a specific Track based on track id
class TrackGetSpecific(Resource):
    method_decorators = [jwt_required, track_exists]

    def get(self, track_id):
        track = Track.query.get(track_id)

        return track_schema.dump(track)


# Creates the routes for the classes
api.add_resource(TrackCRUD, "/tracks")
api.add_resource(TrackFetchAll, "/tracks/all")
api.add_resource(TrackGetSpecific, "/tracks/<int:track_id>")

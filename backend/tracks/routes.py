from flask import (Blueprint)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.tracks.decorators import *
from backend.tracks.schemas import track_schema, tracks_schema
from backend.tracks.utils import create_track, edit_track

# Blueprint for tracks
tracks_bp = Blueprint("tracks", __name__)


# Class for track CRUD routes
class TrackCRUD(Resource):
    method_decorators = [track_exists_in_contentful]

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


# This class is used to delete an track with a POST request
class TrackDelete(Resource):
    method_decorators = [track_delete]

    # Function to delete a track!!
    def post(self):
        contentful_data = request.get_json()
        track = Track.query.filter_by(contentful_id=contentful_data["entityId"]).first()

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
    method_decorators = [track_exists]

    def get(self, track_id):
        track = Track.query.get(track_id)

        return track_schema.dump(track)


# Creates the routes for the classes
api.add_resource(TrackCRUD, "/tracks")
api.add_resource(TrackDelete, "/tracks/delete")
api.add_resource(TrackFetchAll, "/tracks/all")
api.add_resource(TrackGetSpecific, "/tracks/<int:track_id>")

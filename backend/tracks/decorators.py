from flask import request
from backend.models import Track
from functools import wraps
from backend.tracks.schemas import track_form_schema


# Decorator to check if a track exists
def track_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        track = Track.query.get(kwargs['track_id'])

        if track:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Track does not exist"
                   }, 404

    return wrap


# Decorator to check if a track exists in github
def track_exists_in_github(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        track = Track.query.filter_by(github_id=data["github_id"])

        if track:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Track does not exist"
                   }, 404

    return wrap


# Decorator to validate the track form data
def valid_track_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        errors = track_form_schema.validate(data)

        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a track. Double check the JSON data that it has everything needed to create a track."
                   }, 500
        else:
            return f(*args, **kwargs)

    return wrap

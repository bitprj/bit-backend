from flask import request
from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Track
from functools import wraps


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


# Decorator to check if a track exists in contentful
def track_exists_in_contentful(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        content_type = data["contentType"]["sys"]["id"]
        track = Track.query.filter_by(contentful_id=data["entityId"]).first()
        contentful_track = contentful_client.entries(SPACE_ID, 'master').find(data["entityId"])

        # Checks if the track exists in contentful and if its a track
        # Checks if the track exists in the db for put request
        if contentful_track and content_type == "track" or track:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Track does not exist"
                   }, 404

    return wrap


# Decorator to check if the track can be deleted
def track_delete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        track = Track.query.filter_by(contentful_id=data["entityId"]).first()

        if track:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Track does not exist"
                   }, 404

    return wrap

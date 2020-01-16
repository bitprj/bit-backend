from flask import request
from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Activity
from functools import wraps


# Decorator to check if a activity exists
def activity_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        activity = Activity.query.get(kwargs['activity_id'])

        if activity:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Activity does not exist"
                   }, 404

    return wrap


# Decorator to check if a activity exists in contentful
def activity_exists_in_contentful(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        content_type = data["contentType"]["sys"]["id"]
        activity = Activity.query.filter_by(contentful_id=data["entityId"]).first()
        contentful_activity = contentful_client.entries(SPACE_ID, 'master').find(data["entityId"])
        # Checks if the activity exists in contentful and if its a activity
        # Checks if the activity exists in the db for put request
        if contentful_activity and content_type == "activity" or activity:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Activity does not exist"
                   }, 404

    return wrap


# Decorator to check if the activity can be deleted
def activity_delete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        activity = Activity.query.filter_by(contentful_id=data["entityId"]).first()

        if activity:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Activity does not exist"
                   }, 404

    return wrap

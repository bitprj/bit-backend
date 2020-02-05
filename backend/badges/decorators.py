from flask import request
from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Badge
from functools import wraps


# Decorator to check if a badge exists
def badge_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        badge = Badge.query.get(kwargs['badge_id'])

        if badge:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Badge does not exist"
                   }, 404

    return wrap


# Decorator to check if a badge exists in contentful
def badge_exists_in_contentful(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        content_type = data["contentType"]["sys"]["id"]
        badge = Badge.query.filter_by(contentful_id=data["entityId"]).first()
        contentful_badge = contentful_client.entries(SPACE_ID, 'master').find(data["entityId"])
        # Checks if the badge exists in contentful and if its a badge
        # Checks if the badge exists in the db for put request
        if contentful_badge and content_type == "badge" or badge:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Badge does not exist"
                   }, 404

    return wrap


# Decorator to check if the badge can be deleted
def badge_delete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        badge = Badge.query.filter_by(contentful_id=data["entityId"]).first()

        if badge:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Badge does not exist"
                   }, 404

    return wrap


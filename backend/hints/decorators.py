from flask import request
from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Hint
from functools import wraps


# Decorator to check if a hint exists
def hint_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        hint = Hint.query.get(kwargs['hint_id'])

        if hint:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Hint does not exist"
                   }, 404

    return wrap


# Decorator to check if a hint exists in contentful
def hint_exists_in_contentful(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        content_type = data["contentType"]["sys"]["id"]
        hint = Hint.query.filter_by(contentful_id=data["entityId"]).first()
        contentful_hint = contentful_client.entries(SPACE_ID, 'master').find(data["entityId"])
        # Checks if the hint exists in contentful and if its a hint
        # Checks if the hint exists in the db for put request
        if contentful_hint and content_type == "hint" or hint:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Hint does not exist"
                   }, 404

    return wrap


# Decorator to check if the hint can be deleted
def hint_delete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        hint = Hint.query.filter_by(contentful_id=data["entityId"]).first()

        if hint:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Hint does not exist"
                   }, 404

    return wrap

from flask import request
from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Concept
from functools import wraps


# Decorator to check if a concept exists
def concept_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        concept = Concept.query.get(kwargs['concept_id'])

        if concept:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Concept does not exist"
                   }, 404

    return wrap


# Decorator to check if a concept exists in contentful
def concept_exists_in_contentful(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        content_type = data["contentType"]["sys"]["id"]
        concept = Concept.query.filter_by(contentful_id=data["entityId"]).first()
        contentful_concept = contentful_client.entries(SPACE_ID, 'master').find(data["entityId"])
        # Checks if the concept exists in contentful and if its a concept
        # Checks if the concept exists in the db for put request
        if contentful_concept and content_type == "concept" or concept:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Concept does not exist"
                   }, 404

    return wrap


# Decorator to check if the concept can be deleted
def concept_delete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        concept = Concept.query.filter_by(contentful_id=data["entityId"]).first()

        if concept:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Concept does not exist"
                   }, 404

    return wrap

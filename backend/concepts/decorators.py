from flask import request
from backend.concepts.schemas import concept_form_schema
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


# Decorator to check if a module exists in github
def concept_exists_in_github(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        concept = Concept.query.filter_by(filename=data["filename"]).first()

        if concept:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Concept does not exist"
                   }, 404

    return wrap


# Decorator to validate concept form data
def valid_concept_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        errors = concept_form_schema.validate(data)

        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a concept. Double check the JSON data that it has everything needed to create a concept."
                   }, 500
        else:
            return f(*args, **kwargs)

    return wrap

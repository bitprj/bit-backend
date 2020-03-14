from flask import request
from backend import contentful_client
from backend.config import SPACE_ID
from backend.mc_choices.schemas import mc_choice_form_schema
from backend.mc_choices.utils import get_mc_choice
from backend.models import MCChoice
from functools import wraps


# Decorator to check if a mc_choice exists
def mc_choice_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        mc_choice = MCChoice.query.get(kwargs['mc_choice_id'])

        if mc_choice:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "MCChoice does not exist"
                   }, 404

    return wrap


# Decorator to check if a mc_choice exists in github
def mc_choice_exists_in_github(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        mc_choice = get_mc_choice(data)

        if mc_choice:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Checkpoint does not exist"
                   }, 404

    return wrap


# Decorator to check if a mc_choice exists in contentful
def mc_choice_exists_in_contentful(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        content_type = data["contentType"]["sys"]["id"]
        mc_choice = MCChoice.query.filter_by(contentful_id=data["entityId"]).first()
        contentful_mc_choice = contentful_client.entries(SPACE_ID, 'master').find(data["entityId"])
        # Checks if the mc_choice exists in contentful and if its a mc_choice
        # Checks if the mc_choice exists in the db for put request
        if contentful_mc_choice and content_type == "choice" or mc_choice:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "MCChoice does not exist"
                   }, 404

    return wrap


# Decorator to check if the mc_choice can be deleted
def mc_choice_delete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        mc_choice = MCChoice.query.filter_by(contentful_id=data["entityId"]).first()

        if mc_choice:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "MCChoice does not exist"
                   }, 404

    return wrap


# Decorator to validate mc_choice form data
def valid_mc_choice_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        errors = mc_choice_form_schema.validate(data)

        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a mc_choice. Double check the JSON data that it has everything needed to create a mc_choice."
                   }, 500
        else:
            return f(*args, **kwargs)

    return wrap

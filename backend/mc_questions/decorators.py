from flask import request
from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import MCQuestion
from functools import wraps


# Decorator to check if a mc_question exists
def mc_question_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        mc_question = MCQuestion.query.get(kwargs['mc_question_id'])

        if mc_question:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "MCQuestion does not exist"
                   }, 404

    return wrap


# Decorator to check if a mc_question exists in contentful
def mc_question_exists_in_contentful(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        content_type = data["contentType"]["sys"]["id"]
        mc_question = MCQuestion.query.filter_by(contentful_id=data["entityId"]).first()
        contentful_mc_question = contentful_client.entries(SPACE_ID, 'master').find(data["entityId"])
        # Checks if the mc_question exists in contentful and if its a mc_question
        # Checks if the mc_question exists in the db for put request
        if contentful_mc_question and content_type == "mc_question" or mc_question:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "MCQuestion does not exist"
                   }, 404

    return wrap


# Decorator to check if the mc_question can be deleted
def mc_question_delete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        mc_question = MCQuestion.query.filter_by(contentful_id=data["entityId"]).first()

        if mc_question:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "MCQuestion does not exist"
                   }, 404

    return wrap

from flask import request
from backend import contentful_client
from backend.config import SPACE_ID
from backend.general_utils import get_user_id_from_token
from backend.models import Student, Card
from functools import wraps


# Decorator to check if a card exists
def card_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        card = Card.query.get(kwargs['card_id'])

        if card:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Card does not exist"
                   }, 404

    return wrap


# Decorator to check if a card exists in contentful
def card_exists_in_contentful(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        content_type = data["contentType"]["sys"]["id"]
        card = Card.query.filter_by(contentful_id=data["entityId"]).first()
        contentful_card = contentful_client.entries(SPACE_ID, 'master').find(data["entityId"])

        # Checks if the card exists in contentful and if its a card
        # Checks if the card exists in the db for put request
        if contentful_card and content_type == "card" or card:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Card does not exist"
                   }, 404

    return wrap


# Decorator to check if the card can be deleted
def card_delete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        card = Card.query.filter_by(contentful_id=data["entityId"]).first()

        if card:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Card does not exist"
                   }, 404

    return wrap

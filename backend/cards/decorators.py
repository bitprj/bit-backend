from flask import request
from flask_jwt_extended import get_jwt_identity
from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Activity, ActivityProgress, Card, Student
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


# Decorator to check if the card exist in the activity
def card_exists_in_activity(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        card = Card.query.get(kwargs['card_id'])
        activity = Activity.query.get(kwargs['activity_id'])

        if card in activity.cards:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Card does not belong in the activity"
                   }, 404

    return wrap


# Decorator to check if a card is unlockable
def card_is_unlockable(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        card = Card.query.get(kwargs['card_id'])
        student_activity_prog = ActivityProgress.query.filter_by(student_id=student.id,
                                                                 activity_id=kwargs['activity_id']).first()

        if card in student_activity_prog.cards_locked:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Card already unlocked"
                   }, 404

    return wrap

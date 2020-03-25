from flask import (request, session)
from backend.cards.schemas import card_form_schema
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


# Decorator to check if a card exists in github
def card_exists_in_github(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        card = Card.query.filter_by(filename=data["filename"]).first()

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
        username = session["profile"]["username"]
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


# Decorator to validate card form data
def valid_card_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        errors = card_form_schema.validate(data)
        # print(data["name"])
        # print(data)
        # print(errors)

        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a card. Double check the JSON data that it has everything needed to create a card."
                   }, 500
        else:
            return f(*args, **kwargs)

    return wrap

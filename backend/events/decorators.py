from backend.events.schemas import event_form_schema
from backend.models import Event, User
from flask import request, session
from functools import wraps


# Decorator to check if a event exists
def event_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        event = Event.query.get(kwargs['event_id'])

        if event:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Event does not exist"
                   }, 404

    return wrap


# Decorator to check if a user has rsvp'd for an event
# This is used to prevent users from spamming the rsvp button forever....
def has_rsvp(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_data = session["profile"]
        user = User.query.get(user_data["id"])
        event = Event.query.get(kwargs['event_id'])

        if user in event.rsvp_list:
            return {
                       "message": "You already RSVP'd for this event"
                   }, 403
        else:
            return f(*args, **kwargs)

    return wrap


# Function to check if a user in the rsvp list.
# If they are then they can be safely removed from the rsvp list
def in_rsvp(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_data = session["profile"]
        user = User.query.get(user_data["id"])
        event = Event.query.get(kwargs['event_id'])

        if user in event.rsvp_list:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "You can't leave an RSVP if you were not in it in the first place."
                   }, 403

    return wrap


# Decorator to check if a teacher owns a events
# Only owners of the organization or presenters of the event may pass this check
def owns_event(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_data = session["profile"]
        user = User.query.get(user_data["id"])
        event = Event.query.get(kwargs['event_id'])

        if user in event.organization.owners or user in event.presenters:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "You do not own this event"
                   }, 403

    return wrap


# Decorator to check if a event form data is valid
def valid_event_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        form_data = request.get_json()
        errors = event_form_schema.validate(form_data)
        # If form data is not validated by the event_schema, then return a 500 error
        # else create the event and add it to the database
        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a event. Double check the JSON data that it has everything needed to create a event."
                   }, 422
        else:
            return f(*args, **kwargs)

    return wrap

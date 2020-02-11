from backend.authentication.utils import get_users
from backend.models import Event


# Function to create a event
def create_event(form_data, organization_id):
    event = Event(name=form_data["name"],
                  date=form_data["date"],
                  summary=form_data["summary"],
                  location=form_data["location"],
                  organization_id=organization_id
                  )
    event.presenters = get_users(form_data["presenters"])

    return event


# Function to edit a event
def edit_event(event, form_data):
    event.name = form_data["name"]
    event.date = form_data["date"]
    event.summary = form_data["summary"]
    event.location = form_data["location"]
    event.presenters = get_users(form_data["presenters"])

    return

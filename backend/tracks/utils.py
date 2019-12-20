from backend.models import Track
from backend.prereqs.fetch import get_topics


# Function to create a track
def create_track(form_data):
    track = Track(name=form_data["name"],
                  description=form_data["description"],
                  image=form_data["image"]
                  )

    track.topics = get_topics(form_data["topics"])

    return track


# Function to edit a track
def edit_track(track, form_data):
    track.name = form_data["name"]
    track.description = form_data["description"]
    track.image = form_data["image"]
    track.topics = get_topics(form_data["topics"])

    return

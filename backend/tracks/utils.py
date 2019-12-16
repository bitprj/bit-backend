from backend.models import Track


# Function to create a track
def create_track(form_data):
    track = Track(name=form_data["name"])

    return track


# Function to edit a track
def edit_track(track, form_data):
    track.name = form_data["name"]

    return

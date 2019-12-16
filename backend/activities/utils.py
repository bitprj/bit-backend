from backend.models import Activity
from backend.general_utils import add_image


# Function to create a activity
def create_activity(form_data, file_data):
    file = file_data["image"]
    image = add_image(file, "activities")

    activity = Activity(name=form_data["name"],
                        description=form_data["description"],
                        summary=form_data["summary"],
                        difficulty=form_data["difficulty"],
                        image=image
                        )

    return activity


# Function edit a activity
def edit_activity(activity, form_data):
    file = form_data["image"]

    activity.name = form_data["name"]
    activity.description = form_data["description"]
    activity.summary = form_data["summary"]
    activity.difficulty = form_data["difficulty"]
    activity.image = add_image(file, "activities")

    return

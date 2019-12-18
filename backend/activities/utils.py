from backend.models import Activity
from backend.prereqs.fetch import get_modules


# Function to create a activity
def create_activity(form_data):
    activity = Activity(name=form_data["name"],
                        description=form_data["description"],
                        summary=form_data["summary"],
                        difficulty=form_data["difficulty"],
                        image=form_data["image"]
                        )

    activity.modules = get_modules(form_data["module_ids"])

    return activity


# Function edit a activity
def edit_activity(activity, form_data):
    activity.name = form_data["name"]
    activity.description = form_data["description"]
    activity.summary = form_data["summary"]
    activity.difficulty = form_data["difficulty"]
    activity.image = form_data["image"]

    return

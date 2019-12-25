from backend.models import Activity
from backend.prereqs.fetch import get_modules
from backend.prereqs.utils import assign_badge_prereqs, delete_badge_prereqs


# Function to create a activity
def create_activity(form_data):
    activity = Activity(name=form_data["name"],
                        description=form_data["description"],
                        summary=form_data["summary"],
                        difficulty=form_data["difficulty"],
                        image=form_data["image"]
                        )

    activity.modules = get_modules(form_data["modules"])

    return activity


# Function edit a activity
def edit_activity(activity, form_data):
    activity.name = form_data["name"]
    activity.description = form_data["description"]
    activity.summary = form_data["summary"]
    activity.difficulty = form_data["difficulty"]
    activity.image = form_data["image"]
    activity.modules = get_modules(form_data["modules"])
    delete_badge_prereqs(activity)
    assign_badge_prereqs(form_data["badge_prereqs"], activity, "Activity")

    return


# Function to check if a activity exists in the database
def validate_activity(activity_id):
    activity = Activity.query.get(activity_id)

    if not activity:
        return True

    return False

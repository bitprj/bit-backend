# from backend.cards.utils import add_cards
from backend.models import Activity


# Function to create a activity
def create_activity(data):
    activity = Activity(github_id=data["github_id"],
                        filename=data["filename"],
                        name=data["name"],
                        description=data["description"],
                        summary=data["summary"],
                        difficulty=data["difficulty"],
                        image=data["image"]
                        )

    return activity


# Function to edit an activity
def edit_activity(activity, data):
    activity.name = data["name"]
    activity.description = data["description"]
    activity.summary = data["summary"]
    activity.difficulty = data["difficulty"]
    activity.image = data["image"]
    activity.filename = data["filename"]

    return

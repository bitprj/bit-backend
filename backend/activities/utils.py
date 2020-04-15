from backend.concepts.utils import get_concepts
from backend.general_utils import binary_search
from backend.models import Activity, Card, Hint, Module


# Function to add an to a module progress
def add_activity_to_module_progress(student, activity, module_prog):
    if binary_search(student.completed_activities, 0, len(student.completed_activities) - 1, activity.id) != -1:
        module_prog.completed_activities.append(activity)
    elif binary_search(student.incomplete_activities, 0, len(student.incomplete_activities) - 1, activity.id) != -1:
        module_prog.incomplete_activities.append(activity)
    elif binary_search(student.current_activities, 0, len(student.current_activities) - 1, activity.id) != -1:
        module_prog.inprogress_activities.append(activity)
    else:
        student.incomplete_activities.append(activity)
        module_prog.incomplete_activities.append(activity)

    return


# Function to create a activity
def create_activity(data):
    activity = Activity(filename=data["filename"],
                        name=data["name"],
                        description=data["description"],
                        summary=data["summary"],
                        difficulty=data["difficulty"],
                        image=data["image"]
                        )

    activity.is_project = has_hints(data["cards"])

    return activity


# Function to edit an activity
def edit_activity(activity, data):
    activity.name = data["name"]
    activity.description = data["description"]
    activity.summary = data["summary"]
    activity.difficulty = data["difficulty"]
    activity.image = data["image"]
    activity.filename = data["filename"]
    activity.is_project = has_hints(data["cards"])

    if "cards" in data:
        card_filename_path = activity.filename.split("/")[:-1]
        card_path = "/".join(card_filename_path)

        for card_name, card_data in data["cards"].items():
            card_filename = card_path + "/cards/" + card_name + ".md"
            update_card(card_data, card_name, card_filename)

    return


# Function to get the list of activities based on the activity filepath
def get_activities(activity_paths):
    activities = []

    for activity_path in activity_paths:
        activity = Activity.query.filter_by(filename=activity_path + "/README.md").first()
        activities.append(activity)

    return activities


# Function to get the activity_paths from a module README
def get_activity_paths(data):
    activity_paths = []

    if "activities" in data:
        activity_paths += data["activities"]
    if "projects" in data:
        activity_paths += data["projects"]

    return activity_paths


# Function to check if the activity's cards have hints
def has_hints(cards):
    for card in cards.keys():
        if len(card) > 2:
            return True

    return False


# Function to update an Activity's cards/hints from the README when the
# Activity gets updated
def update_card(card_data, card_name, card_filename):
    card = None

    if len(card_name) <= 2:
        card = Card.query.filter_by(filename=card_filename).first()
    else:
        card = Hint.query.filter_by(filename=card_filename).first()

    if card:
        card.name = card_data["name"]
        card.order = card_data["order"]
        card.gems = card_data["gems"]

        if "concepts" in card_data:
            card.concepts = get_concepts(card_data["concepts"], card)

    return


# Function to update activity_prereqs
def update_prereqs(activities):
    prereqs = []

    for activity_id in activities:
        activity = Activity.query.filter_by(github_id=int(activity_id)).first()
        if activity:
            prereqs.append(activity)

    return prereqs

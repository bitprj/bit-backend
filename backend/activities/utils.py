from backend.concepts.utils import get_concepts
from backend.models import Activity, Card, Hint, Module


# Function to assign an activity to a module
def assign_activity_to_module(filename, activity):
    activity_path = filename.split("/")
    module_path = "/".join(activity_path[:-2]) + "/README.md"
    module = Module.query.filter_by(filename=module_path).first()
    module.activities.append(activity)

    return


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

    activity.is_project = has_hints(data["cards"])
    assign_activity_to_module(data["filename"], activity)

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
    assign_activity_to_module(data["filename"], activity)

    if "cards" in data:
        card_filename_path = activity.filename.split("/")[:-1]
        card_path = "/".join(card_filename_path)

        for card_name, card_data in data["cards"].items():
            card_filename = card_path + "/cards/" + card_name + ".md"
            update_card(card_data, card_name, card_filename)

    return


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

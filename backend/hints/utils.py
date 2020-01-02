from backend.models import Hint
from backend.steps.utils import delete_steps, generate_steps


# Function to create a hint
def create_hint(contentful_data):
    hint = Hint(contentful_data["entityId"]
                )

    # hint.card_id = card_id
    # hint.steps = generate_steps((contentful_data["steps"]))

    return hint


# Function to edit a hint
def edit_hint(hint, contentful_data):
    hint.name = contentful_data["parameters"]["name"]["en-US"]
    # hint.parent = contentful_data["parent"]
    # delete_steps(hint.steps)
    # hint.steps = generate_steps((contentful_data["steps"]))

    return

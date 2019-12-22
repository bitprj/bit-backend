from backend.models import Hint
from backend.steps.utils import delete_steps, generate_steps


# Function to create a hint
def create_hint(form_data, card_id):
    hint = Hint(name=form_data["name"],
                difficulty=form_data["difficulty"],
                gems=form_data["gems"],
                parent=form_data["parent"]
                )

    hint.card_id = card_id
    hint.steps = generate_steps((form_data["steps"]))

    return hint


# Function to edit a hint
def edit_hint(hint, form_data):
    hint.name = form_data["name"]
    hint.difficulty = form_data["difficulty"]
    hint.gems = form_data["gems"]
    hint.parent = form_data["parent"]
    delete_steps(hint.steps)
    hint.steps = generate_steps((form_data["steps"]))

    return

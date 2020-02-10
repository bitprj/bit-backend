from backend import contentful_client, db
from backend.config import SPACE_ID
from backend.models import Hint, HintStatus
from backend.prereqs.fetch import get_steps


# Function to assign children hints to a parent
def assign_hints_to_parent_hint(children_hints):
    hints = []

    for hint in children_hints:
        target_hint = Hint.query.filter_by(contentful_id=hint["sys"]["id"]).first()
        hints.append(target_hint)

    return hints


# Function to create a hint
def create_hint(contentful_data):
    hint = Hint(contentful_data["entityId"]
                )

    return hint


# Function to create a list of HintStatus Models based on an array of hints
def create_hint_status(activity_prog, hints):
    for hint in hints:
        hint_status = HintStatus(activity_progress_id=activity_prog.id,
                                 is_unlocked=False,
                                 card_id=hint.card_id)
        hint_status.hint = hint

        db.session.commit()

        for children_hint in hint.hint_children:
            child_hint_status = HintStatus(activity_progress_id=activity_prog.id,
                                           parent_hint_id=hint_status.id,
                                           is_unlocked=False)
            child_hint_status.hint = children_hint

    return


# Function to delete a hint's relationship
def delete_hint(hint):
    # Deletes the hint's steps in contentful
    for step in hint.steps:
        # Unpublishes the steps first then deletes the step in contentful
        step_entry = contentful_client.entries(SPACE_ID, 'master').find(step.contentful_id)
        step_entry.unpublish()
        contentful_client.entries(SPACE_ID, 'master').delete(step.contentful_id)

    return


# Function to edit a hint
def edit_hint(hint, contentful_data):
    hint.name = contentful_data["parameters"]["name"]["en-US"]
    hint.steps = get_steps(contentful_data["parameters"]["steps"]["en-US"])
    hint.gems = contentful_data["parameters"]["gems"]["en-US"]

    if "children_hints" in contentful_data["parameters"]:
        hint.hint_children = assign_hints_to_parent_hint(contentful_data["parameters"]["children_hints"]["en-US"])

    return


# Function to validate a hint
def validate_hint(hint_id):
    hint = Hint.query.get(hint_id)

    if not hint:
        return False

    return True

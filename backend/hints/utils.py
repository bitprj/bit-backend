from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Hint
from backend.prereqs.fetch import get_steps
from backend.steps.utils import delete_steps, generate_steps


# Function to create a hint
def create_hint(contentful_data):
    hint = Hint(contentful_data["entityId"]
                )

    return hint


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

    return

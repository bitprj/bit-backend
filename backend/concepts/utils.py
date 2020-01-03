from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Concept
from backend.prereqs.fetch import get_steps


# Function to create a concept
def create_concept(contentful_data):
    concept = Concept(contentful_data["entityId"])

    return concept


# Function to delete a concept's relationship
def delete_concept(concept):
    # Deletes the concept steps in contentful
    for step in concept.steps:
        # Unpublishes the steps first then deletes the step in contentful
        step_entry = contentful_client.entries(SPACE_ID, 'master').find(step.contentful_id)
        step_entry.unpublish()
        contentful_client.entries(SPACE_ID, 'master').delete(step.contentful_id)

    return


# Function to edit a concept
def edit_concept(concept, contentful_data):
    concept.name = contentful_data["parameters"]["name"]["en-US"]
    concept.steps = get_steps((contentful_data["parameters"]["steps"]["en-US"]))

    return

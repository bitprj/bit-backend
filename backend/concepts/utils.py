from backend.models import Concept
from backend.prereqs.fetch import get_cards
from backend.steps.utils import delete_steps, generate_steps


# Function to create a concept
def create_concept(contentful_data):
    concept = Concept(contentful_data["entityId"])
    # concept.cards = get_cards(contentful_data["cards"])
    # concept.steps = generate_steps((contentful_data["steps"]))

    return concept


# Function to edit a concept
def edit_concept(concept, contentful_data):
    concept.name = contentful_data["parameters"]["name"]["en-US"]
    # delete_steps(concept.steps)
    # concept.steps = generate_steps((contentful_data["steps"]))

    return

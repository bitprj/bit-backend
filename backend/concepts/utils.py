from backend.models import Concept
from backend.steps.utils import generate_steps
from backend.prereqs.fetch import get_cards


# Function to create a concept
def create_concept(form_data):
    concept = Concept(name=form_data["name"])
    concept.cards = get_cards(form_data["cards"])
    concept.steps = generate_steps((form_data["steps"]))

    return concept


# Function to edit a concept
def edit_concept(concept, form_data):
    concept.name = form_data["name"]
    concept.cards = get_cards(form_data["cards"])
    concept.steps = generate_steps((form_data["steps"]))

    return

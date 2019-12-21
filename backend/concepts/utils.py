from backend.models import Concept
from backend.prereqs.fetch import get_cards
from backend.steps.utils import delete_steps, generate_steps


# Function to create a concept
def create_concept(form_data):
    concept = Concept(name=form_data["name"])
    concept.cards = get_cards(form_data["cards"])
    concept.steps = generate_steps((form_data["steps"]))

    return concept


# Function to edit a concept
def edit_concept(concept, form_data):
    concept.name = form_data["name"]
    delete_steps(concept.steps)
    concept.steps = generate_steps((form_data["steps"]))

    return

from backend.models import Card
from backend.prereqs.fetch import get_concepts


# Function to create a card
def create_card(contentful_data):
    card = Card(contentful_id=contentful_data["entityId"]
                )

    return card


# Function to edit a card
def edit_card(card, contentful_data):
    card.name = contentful_data["parameters"]["name"]["en-US"]
    # card.concepts = get_concepts(form_data["concepts"])

    return

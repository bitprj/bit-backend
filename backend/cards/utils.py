from backend.models import Card
from backend.prereqs.fetch import get_concepts


# Function to create a card
def create_card(form_data, activity_id):
    card = Card(name=form_data["name"],
                md_file=form_data["md_file"],
                gems=form_data["gems"],
                activity_id=activity_id
                )

    return card


# Function to edit a card
def edit_card(card, form_data):
    card.name = form_data["name"]
    card.md_file = form_data["md_file"]
    card.gems = form_data["gems"]
    card.concepts = get_concepts(form_data["concepts"])

    return

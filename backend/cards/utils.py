from backend import contentful_client
from backend.models import Card
from backend.config import SPACE_ID
from backend.hints.utils import get_hint_children
from backend.prereqs.fetch import get_concepts, get_hints


# Function to create a card
def create_card(contentful_data):
    card = Card(contentful_id=contentful_data["entityId"]
                )

    return card


# Function to delete a card's relationships
def delete_card(card):
    card.concepts = []

    # This is used to delete all the hints in a card in contentful
    for hint in card.hints:
        # Unpublished the hint first then deletes the hint in contentful
        hint_entry = contentful_client.entries(SPACE_ID, 'master').find(hint.contentful_id)
        hint_entry.unpublish()
        contentful_client.entries(SPACE_ID, 'master').delete(hint.contentful_id)

    return


# Function to edit a card
def edit_card(card, contentful_data):
    card.name = contentful_data["parameters"]["name"]["en-US"]
    card.order = contentful_data["parameters"]["order"]["en-US"]

    if "concepts" in contentful_data["parameters"]:
        card.concepts = get_concepts(contentful_data["parameters"]["concepts"]["en-US"])

    if "hints" in contentful_data["parameters"]:
        card.hints = get_hints(contentful_data["parameters"]["hints"]["en-US"])

    return


# Function to get all the card's hints
def get_cards_hints(cards):
    hints = []
    all_hints = []

    for card in cards:
        hints += card.hints

    # gets the hint's children hints and adds it to all_hints
    all_hints += get_hint_children(hints)

    return all_hints

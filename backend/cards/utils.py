from backend import contentful_client
from backend.checkpoints.utils import delete_checkpoint
from backend.config import SPACE_ID
from backend.models import Card, Checkpoint
from backend.prereqs.fetch import get_concepts, get_hints


# Function to add cards to activities
def add_cards(card_data):
    cards = []

    for card_name, card_val in card_data.items():
        if len(card_name) == 1:
            card = Card.query.filter_by(github_raw_data=card_val["github_raw_data"]).first()
            cards.append(card)

    return cards


# Function to create a card
def create_card(data):
    card = Card(github_raw_data=data["github_raw_data"],
                name=data["name"],
                gems=data["gems"],
                order=data["order"],
                filename=data["filename"]
                )

    return card


# Function to delete a card's relationships
def delete_card(card, checkpoint):
    card.concepts = []

    if checkpoint:
        delete_checkpoint(checkpoint)

    # This is used to delete all the hints in a card in contentful
    for hint in card.hints:
        # Unpublished the hint first then deletes the hint in contentful
        hint_entry = contentful_client.entries(SPACE_ID, 'master').find(hint.contentful_id)
        hint_entry.unpublish()
        contentful_client.entries(SPACE_ID, 'master').delete(hint.contentful_id)

    return


# Function to edit a card
def edit_card(card, data):
    card.github_raw_data = data["github_raw_data"]
    card.name = data["name"]
    card.order = data["order"]
    card.gems = data["gems"]
    card.filename = data["filename"]

    # if "checkpoint" in data["parameters"]:
    #     checkpoint = Checkpoint.query.filter_by(
    #         id=data["parameters"]["checkpoint"]["en-US"]["sys"]["id"]).first()
    #     card.checkpoint_id = checkpoint.id
    #
    # if "concepts" in data["parameters"]:
    #     card.concepts = get_concepts(data["parameters"]["concepts"]["en-US"])
    #
    # if "hints" in data["parameters"]:
    #     card.hints = get_hints(data["parameters"]["hints"]["en-US"])

    return


# Function to get all the card's hints
def get_cards_hints(cards):
    hints = []

    for card in cards:
        hints += card.hints

    return hints

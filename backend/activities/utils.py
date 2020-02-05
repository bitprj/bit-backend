from backend import contentful_client
from backend.cards.utils import add_cards, delete_card
from backend.config import SPACE_ID
from backend.models import Activity


# Function to create a activity
def create_activity(contentful_data):
    activity = Activity(contentful_id=contentful_data["entityId"]
                        )

    return activity


# Function to delete an activity's cards
def delete_cards(cards):
    for card in cards:
        delete_card(card, card.checkpoint)

        # Unpublishes the card first then deletes the card in contentful
        card_entry = contentful_client.entries(SPACE_ID, 'master').find(card.contentful_id)
        card_entry.unpublish()
        contentful_client.entries(SPACE_ID, 'master').delete(card.contentful_id)

    return


# Function to edit an activity
def edit_activity(activity, contentful_data):
    activity.name = contentful_data["parameters"]["name"]["en-US"]
    activity.cards = add_cards(contentful_data)

    return


# Function to validate an activity
def validate_activity(activity_id):
    activity = Activity.query.get(activity_id)

    if not activity:
        return True

    return False

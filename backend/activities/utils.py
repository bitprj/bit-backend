from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Activity, Card, Checkpoint


# Function to add cards to activities
def add_cards(activity, contentful_data):
    card_list = contentful_data["parameters"]["cards"]["en-US"]
    cards = []

    if card_list:
        for card in card_list:
            contentful_id = card["sys"]["id"]
            target_card = Card.query.filter_by(contentful_id=contentful_id).first()
            cards.append(target_card)

    activity.cards = cards

    return


# Function to add checkpoints to activities
def add_checkpoints(activity, contentful_data):
    checkpoint_list = contentful_data["parameters"]["checkpoints"]["en-US"]
    checkpoints = []

    if checkpoint_list:
        for checkpoint in checkpoint_list:
            contentful_id = checkpoint["sys"]["id"]
            target_checkpoint = Checkpoint.query.filter_by(contentful_id=contentful_id).first()
            checkpoints.append(target_checkpoint)

    activity.checkpoints = checkpoints

    return


# Function to create a activity
def create_activity(contentful_data):
    activity = Activity(contentful_id=contentful_data["entityId"]
                        )

    return activity


# Function to delete an activity's cards
def delete_cards(cards):
    for card in cards:
        # Unpublishes the card first then deletes the card in contentful
        card_entry = contentful_client.entries(SPACE_ID, 'master').find(card.contentful_id)
        card_entry.unpublish()
        contentful_client.entries(SPACE_ID, 'master').delete(card.contentful_id)

    return


# Function to delete an activity's checkpoints
def delete_checkpoints(checkpoints):
    for checkpoint in checkpoints:
        # Unpublishes the checkpoint first then deletes the checkpoint in contentful
        checkpoint_entry = contentful_client.entries(SPACE_ID, 'master').find(checkpoint.contentful_id)
        checkpoint_entry.unpublish()
        contentful_client.entries(SPACE_ID, 'master').delete(checkpoint.contentful_id)

    return


# Function to edit an activity
def edit_activity(activity, contentful_data):
    activity.name = contentful_data["parameters"]["name"]["en-US"]
    add_cards(activity, contentful_data)
    add_checkpoints(activity, contentful_data)

    return


# Function to validate an activity
def validate_activity(activity_id):
    activity = Activity.query.get(activity_id)

    if not activity:
        return True

    return False

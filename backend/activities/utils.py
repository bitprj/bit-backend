from backend import contentful_client, repo
from backend.cards.utils import add_cards, delete_card
from backend.config import SPACE_ID
from backend.models import Activity


# Function to create a activity
def create_activity(data):
    activity = Activity(github_id=data["github_id"],
                        name=data["name"],
                        description=data["description"],
                        summary=data["summary"],
                        difficulty=data["difficulty"],
                        image=data["image"]
                        )
    contents = repo.get_contents(path=data["folder_location"])

    cards = {}
    for content in contents:
        card_name = content.path.split("/")[2]
        cards[card_name] = content.download_url

    # activity.cards = add_cards(data)

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
def edit_activity(activity, data):
    activity.github_id = data["github_id"]
    activity.name = data["name"]
    activity.description = data["description"]
    activity.summary = data["summary"]
    activity.difficulty = data["difficulty"]
    activity.image = data["image"]
    # activity.cards = add_cards(data)

    return

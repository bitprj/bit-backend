from backend import db
from backend.general_utils import create_schema_json, send_file_to_cdn
from backend.general_utils import create_schema_json
from backend.models import Card
import requests


# Function to create a card
def create_card(data, activity_id):
    card = Card(github_raw_data=data["github_raw_data"],
                name=data["name"],
                gems=data["gems"],
                order=data["order"],
                filename=data["filename"],
                activity_id=activity_id
                )
    github_data = requests.get(data["github_raw_data"])
    card.content = github_data.text

    return card


# Function to create a card's md file and send them to s3
def create_md_file(card):
    file_path = card.filename.split("/")
    card_path = "/".join(file_path[:-1])
    card_name = file_path[-1]
    content_md_url = send_file_to_cdn(card.github_raw_data, card_path, card_name)

    return content_md_url


# Function to edit a card
def edit_card(card, data):
    card.name = data["name"]
    card.order = data["order"]
    card.gems = data["gems"]
    card.github_raw_data = data["github_raw_data"]
    github_data = requests.get(data["github_raw_data"])
    card.content = github_data.text
    card.content_url = create_schema_json(card, "card")

    return


# Function to get all the card's hints
def get_cards_hints(cards):
    hints = []

    for card in cards:
        hints += card.hints

    return hints


# Function to update all of the cards associated with a concept
def update_card_cdn(cards):
    for card in cards:
        card.content_url = create_schema_json(card, "card")

    db.session.commit()

    return

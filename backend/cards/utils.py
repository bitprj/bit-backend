from backend import db
from backend.general_utils import create_image_obj, create_schema_json, get_base_folder, send_file_to_cdn
from backend.models import Card
from bs4 import BeautifulSoup
import requests
import uuid


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
    card.content = update_card_images(github_data.text, data["filename"])

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
    card.content = update_card_images(github_data.text, data["filename"])
    create_schema_json(card, "cards")

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
        create_schema_json(card, "cards")

    db.session.commit()

    return


# Function to update the cards images with S3 links
def update_card_images(html, filename):
    soup = BeautifulSoup(html, features="html.parser")
    card_base_file = get_base_folder(filename)

    for img in soup.findAll('img'):
        if "https" not in img["src"]:
            image_path = img["src"].split("/")
            image_folder = card_base_file + "/" + "/".join(image_path[1:3])
            unique_str = str(uuid.uuid1())
            img["src"] = create_image_obj(unique_str + image_path[2], image_folder, "cards")

    return str(soup.prettify(formatter=None))

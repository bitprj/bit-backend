from backend.models import Card


# Function to create a card
def create_card(data, activity_id):
    card = Card(github_raw_data=data["github_raw_data"],
                name=data["name"],
                gems=data["gems"],
                order=data["order"],
                filename=data["filename"],
                activity_id=activity_id
                )

    return card


# Function to edit a card
def edit_card(card, data):
    card.name = data["name"]
    card.order = data["order"]
    card.gems = data["gems"]
    card.github_raw_data = data["github_raw_data"]

    # if "checkpoint" in data["parameters"]:
    #     checkpoint = Checkpoint.query.filter_by(
    #         id=data["parameters"]["checkpoint"]["en-US"]["sys"]["id"]).first()
    #     card.checkpoint_id = checkpoint.id
    #
    # if "concepts" in data["parameters"]:
    #     card.concepts = get_concepts(data["parameters"]["concepts"]["en-US"])

    return


# Function to get all the card's hints
def get_cards_hints(cards):
    hints = []

    for card in cards:
        hints += card.hints

    return hints

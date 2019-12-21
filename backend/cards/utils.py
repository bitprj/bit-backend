from backend.models import Card


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

    return

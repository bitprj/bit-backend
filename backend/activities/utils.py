from backend.models import Activity, Card


# Function to add cards to activities
def add_cards(activity, contentful_data):
    cards = []

    if contentful_data["cards"]:
        for card in contentful_data["cards"]:
            target_card = Card.query.filter_by(name=card.name).first()
            cards.append(target_card)

    activity.cards = cards

    return


# Function to create a activity
def create_activity(contentful_data):
    activity = Activity(contentful_id=contentful_data["entityId"]
                        )

    return activity


# Function to edit an activity
def edit_activity(contentful_data):
    activity = Activity.query.filter_by(contentful_id=contentful_data["entityId"]).first()
    activity.name = contentful_data["parameters"]["name"]["en-US"]
    add_cards(activity, contentful_data)
    
    return

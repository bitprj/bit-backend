from backend.models import Activity, Badge, Card, Module, Topic


# Function to check if the list of activity_ids are valid in the database
def validate_activities(activity_ids):
    for activity_id in activity_ids:
        activity = Activity.query.get(activity_id)

        if not activity:
            return True

    return False


# Function to check if the list of badge_ids are valid in the database
def validate_badges(badge_data):
    for badge_info in badge_data:
        badge = Badge.query.get(badge_info["id"])

        if not badge:
            return True

    return False


# Function to check if the list of card_ids are valid in the database
def validate_cards(card_ids):
    for card_id in card_ids:
        card = Card.query.get(card_id)

        if not card:
            return True

    return False


# Function to check if the list of module_ids are valid in the database
def validate_modules(module_ids):
    for module_id in module_ids:
        module = Module.query.get(module_id)

        if not module:
            return True

    return False


# Function to check if the list of topic_ids are valid in the database
def validate_topics(topic_ids):
    for topic_id in topic_ids:
        topic = Topic.query.get(topic_id)

        if not topic:
            return True

    return False

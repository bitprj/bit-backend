from backend.models import Activity, Card, Concept, Module, Topic


# Function to return a list of activities based on a list of activity ids
def get_activities(activity_list):
    activities = []

    for activity_id in activity_list:
        activity = Activity.query.filter_by(contentful_id=activity_id["sys"]["id"]).first()
        activities.append(activity)

    return activities


# Function to return a list of cards based on a list of card ids
def get_cards(card_ids):
    cards = []

    for card_id in card_ids:
        card = Card.query.get(card_id)
        cards.append(card)

    return cards


# Function to return a list of concepts from a list of concept ids
def get_concepts(concept_ids):
    concepts = []

    for concept_id in concept_ids:
        concept = Concept.query.get(concept_id)
        concepts.append(concept)

    return concepts


# Function to return a list of modules based on a list of module ids
def get_modules(module_list):
    modules = []

    for module_id in module_list:
        module = Module.query.filter_by(contentful_id=module_id["sys"]["id"]).first()
        modules.append(module)

    return modules


# Function to return a list of topics based on the contentful jds
def get_topics(topic_list):
    topics = []

    for topic_id in topic_list:
        topic = Topic.query.filter_by(contentful_id=topic_id["sys"]["id"]).first()
        topics.append(topic)

    return topics

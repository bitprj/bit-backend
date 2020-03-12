from backend.models import Activity, Card, Concept, Hint, MCChoice, Module, Step, Topic


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


# Function to return a list of mc_choices from a list of mc_choice ids
def get_mc_choices(mc_choice_list):
    mc_choices = []

    for mc_choice_id in mc_choice_list:
        mc_choice = MCChoice.query.filter_by(contentful_id=mc_choice_id["sys"]["id"]).first()
        mc_choices.append(mc_choice)

    return mc_choices


# Function to return a list of concepts from a list of concept ids
def get_concepts(concept_list):
    concepts = []

    for concept_id in concept_list:
        concept = Concept.query.filter_by(contentful_id=concept_id["sys"]["id"]).first()
        concepts.append(concept)

    return concepts


# Function to return a list of hints from a list of hint ids
def get_hints(hint_list):
    hints = []

    for hint_id in hint_list:
        hint = Hint.query.filter_by(contentful_id=hint_id["sys"]["id"]).first()
        hints.append(hint)

    return hints


# Function to return a list of modules based on a list of module github_ids
def get_modules(module_list):
    modules = []

    for module_filename in module_list:
        filename = module_filename + "/README.md"
        module = Module.query.filter_by(filename=filename).first()
        modules.append(module)

    return modules


# Function to return a list of steps based on a list of step ids
def get_steps(step_list):
    steps = []

    for step_id in step_list:
        step = Step.query.filter_by(contentful_id=step_id["sys"]["id"]).first()
        steps.append(step)

    return steps


# Function to return a list of topics based on the github_ids
def get_topics(topic_list):
    topics = []

    for topic in topic_list:
        topic = Topic.query.filter_by(github_id=topic["github_id"]).first()
        topics.append(topic)

    return topics

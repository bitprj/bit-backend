from backend import repo
from backend.hooks.utils import md_to_json, parse_activity, parse_card, parse_checkpoint, parse_concept, parse_module, \
    parse_topic
from backend.hooks.update_utils import update_cdn_data, update_test_cases


# Function to take all the files changed from commits into specific lists
def store_files(files_to_change):
    topic_files = []
    module_files = []
    activity_files = []
    concept_files = []
    card_files = []
    checkpoint_files = []
    tests_cases = set()

    for file in files_to_change.values():
        if len(file.filename.split("/")) == 2 and "README.md" in file.filename and file.filename.endswith(".md"):
            topic_files.append(file)

        if len(file.filename.split("/")) == 3 and "Modules" in file.filename and file.filename.endswith(".md"):
            module_files.append(file)

        if "Module" in file.filename and (
                "Activity" in file.filename or "Lab" in file.filename) and "README.md" in file.filename:
            activity_files.append(file)

        if "concepts" in file.filename and "images" not in file.filename:
            concept_files.append(file)

        if "Topic" in file.filename and "Module" in file.filename and (
                "Activity" in file.filename or "Lab" in file.filename) and "cards" in file.filename and file.filename.endswith(
                ".md"):
            card_files.append(file)

        if "Module" in file.filename and (
                "Activity" in file.filename or "Lab" in file.filename) and "checkpoints" in file.filename:
            checkpoint_files.append(file)

        if "Topic" in file.filename and "Module" in file.filename and ("Activity" in file.filename or "Lab" in file.filename) and "tests" in file.filename:
            name = file.filename.split("/")
            test_location = "/".join(name[:-1])
            test_location += "/"
            tests_cases.add(test_location)

    card_files.sort(key=lambda x: x.filename, reverse=True)

    return topic_files, module_files, activity_files, concept_files, card_files, checkpoint_files, tests_cases


# Function to parse files
def parse_files(topic_files, module_files, activity_files, concept_files, card_files, checkpoint_files,
                test_case_files):
    # Activity cards is used to get the card dictionary if their cards get updated
    activity_cards = {}
    for file in module_files:
        parse_module(file)

    for file in topic_files:
        parse_topic(file)

    for file in concept_files:
        parse_concept(file)

    for file in activity_files:
        cards = parse_activity(file)
        activity_name = file.filename.split("/")
        activity_path = "/".join(activity_name[:-1]) + "/README.md"
        activity_cards[activity_path] = cards

    for file in card_files:
        card_name = file.filename.split("/")
        parent_path = "/".join(card_name[:-2]) + "/README.md"

        # Gets the card dictionary from github from the activity README
        if parent_path in activity_cards:
            parse_card(file, activity_cards[parent_path], parent_path)
        else:
            # gets the cards from the updated activity README
            activity_readme = repo.get_contents(parent_path)
            cards = md_to_json(activity_readme.download_url)["cards"]
            parse_card(file, cards, parent_path)

    for file in test_case_files:
        update_test_cases(file[:-1])

    for file in checkpoint_files:
        parse_checkpoint(file)

    # Update the activity, card, hints,  cdn data
    for file in activity_files:
        update_cdn_data(file)

    return

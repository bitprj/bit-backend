from backend import repo
from backend.hooks.utils import md_to_json, parse_activity, parse_card, parse_concept, parse_module, parse_tracks


# Function to take all the files changed from commits into specific lists
def store_files(files_to_change):
    module_files = []
    activity_files = []
    concept_files = []
    card_files = []

    for file in files_to_change.values():
        if "Module" in file.filename and "Activity" not in file.filename and "README.md" in file.filename:
            module_files.append(file)

        if "Module" in file.filename and "Activity" in file.filename and "README.md" in file.filename:
            activity_files.append(file)

        if "Concepts" in file.filename and "images" not in file.filename:
            concept_files.append(file)

        if "Module" in file.filename and "Activity" in file.filename and "Cards" in file.filename and file.filename.endswith(
                ".md"):
            card_files.append(file)
    card_files.sort(key=lambda x: x.filename, reverse=True)

    return module_files, activity_files, concept_files, card_files


# Function to parse files
def parse_files(module_files, activity_files, concept_files, card_files):
    activity_cards = {}

    for file in module_files:
        parse_module(file)

    for file in activity_files:
        cards = parse_activity(file)
        activity_name = file.filename.split("/")
        activity_path = "/".join(activity_name[:-1]) + "/README.md"
        activity_cards[activity_path] = cards

    for file in concept_files:
        parse_concept(file)

    for file in card_files:
        card_name = file.filename.split("/")
        parent_path = "/".join(card_name[:-2]) + "/README.md"

        if parent_path in activity_cards:
            parse_card(file, activity_cards[parent_path], parent_path)
        else:
            activity_readme = repo.get_contents(parent_path)
            cards = md_to_json(activity_readme.download_url)["cards"]
            parse_card(file, cards, parent_path)

    return

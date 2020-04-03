from backend import db
from backend.general_utils import create_zip, delete_files, parse_img_tag, create_schema_json, send_tests_zip
from backend.models import Activity, Checkpoint
import backend.activities as activity_utils
import backend.hooks as hook_utils
import requests


# Function to update card data
def update_card_data(file, activity_cards):
    # Gets the card name
    card_path = file.filename.split("/")
    card_file = card_path[-1]
    card_name = card_file.split(".")[0]
    card_data = activity_cards[card_name]
    # Edit card_data
    card_data["gems"] = int(card_data["gems"])
    card_data["order"] = int(card_data["order"])
    card_data["filename"] = file.filename
    card_data["github_raw_data"] = file.raw_url

    return card_data, card_name


# Function to update cdn data
# When all models are done updating, then the activity, cards,
# concepts and checkpoints get updated
def update_cdn_data(file):
    activity = Activity.query.filter_by(filename=file.filename).first()
    data = hook_utils.utils.md_to_json(file.raw_url)

    if "activity_prerequisites" in data:
        activity.prerequisite_activities = activity_utils.utils.update_prereqs(data["activity_prerequisites"])

    activity.content_url = create_schema_json(activity, "activity")

    for module in activity.modules:
        module.content_url = create_schema_json(module, "module")

    for card in activity.cards:
        github_data = requests.get(card.github_raw_data)
        card.content = github_data.text
        card.content_url = create_schema_json(card, "card")
        if card.hints:
            update_hint_cdn(card.hints)

    db.session.commit()

    return


def update_hint_cdn(hints):
    for hint in hints:
        hint.content_url = create_schema_json(hint, "hint")

        if hint.hints:
            update_hint_cdn(hint.hints)

    return


# Function to update hint data
def update_hint_data(hint_data, hint_name):
    # gets the last element in the list which is the hint name
    split_child = hint_data["filename"].split("/")
    hint_path = split_child[-1].split(".")[0]
    parent_length = len(hint_path) - 2
    parent_name = hint_name[:parent_length]
    # Gets the parent filename
    hint_data["parent_filename"] = "/".join(split_child[:-1]) + "/" + parent_name + ".md"

    # This is used to determine if the hint's parent is a card or hint
    if parent_length == 1:
        hint_data["is_card_hint"] = True
    else:
        hint_data["is_card_hint"] = False

    return hint_data


# Function to update step data
def update_step_data(step_data, data, key, parent_id, parent_type):
    # Gives the step a unique key to reference later
    step_data["step_key"] = key

    if "image_folder" in data:
        step_data["image_folder"] = data["image_folder"]

    # If the step is for a concept make the parent a concept
    if parent_type == "concept":
        step_data["concept_id"] = parent_id
        step_data["type"] = "concept"

    # If the step is for a hint make the parent a hint
    elif parent_type == "hint":
        step_data["hint_id"] = parent_id
        step_data["type"] = "hint"

    return step_data


# Function to type cast module fields and update image field
def update_module_data(data):
    data["image"] = parse_img_tag(data["image"], data["image_folder"], "modules")

    # Type casting strings to ints bc they are interpreted as strings
    # when parsed
    if "gems_needed" in data:
        data["gems_needed"] = int(data["gems_needed"])

    if "github_id" in data:
        data["github_id"] = int(data["github_id"])

    return data


# Function to update tests.zip files
def update_test_cases(test_case_location):
    checkpoints = Checkpoint.query.filter_by(test_cases_location=test_case_location).all()

    for checkpoint in checkpoints:
        # Recreates a tests.zip file and sends it to s3
        files = create_zip(test_case_location)
        zip_link = send_tests_zip(checkpoint.filename)
        delete_files(files)
        checkpoint.tests_zip = zip_link
    db.session.commit()

    return


# Function to type cast topic fields
def update_topic_data(data, file):
    data["github_id"] = int(data["github_id"])
    data["image"] = parse_img_tag(data["image"], data["image_folder"], "topics")
    data["filename"] = file.filename

    for i in range(len(data["modules"]) - 1):
        data["modules"][i] = int(data["modules"][i])

    return data

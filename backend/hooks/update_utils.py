from backend import db
from backend.general_utils import create_zip, delete_files, parse_img_tag, send_tests_zip
from backend.models import Checkpoint


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


# Function to update hint data
def update_hint_data(hint_data, hint_name, content):
    # gets the last element in the list which is the card/hint name
    split_child = hint_data["filename"].split("/")
    hint_path = split_child[-1].split(".")[0]
    parent_length = len(hint_path) - 2
    parent_name = hint_name[:parent_length]
    hint_data["parent_filename"] = "/".join(split_child[:-1]) + "/" + parent_name + ".md"
    hint_data["content"] = content

    # This is used to determine if the hint's parent is a card or hint
    if parent_length == 1:
        hint_data["is_card_hint"] = True
    else:
        hint_data["is_card_hint"] = False

    return hint_data


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
        files = create_zip(test_case_location)
        zip_link = send_tests_zip(checkpoint.filename)
        delete_files(files)
        checkpoint.tests_zip = zip_link
    db.session.commit()

    return


# Function to type case topic fields
def update_topic_data(data, file):
    data["github_id"] = int(data["github_id"])
    data["image"] = parse_img_tag(data["image"], data["image_folder"], "topics")
    data["filename"] = file.filename

    for i in range(len(data["modules"]) - 1):
        data["modules"][i] = int(data["modules"][i])

    return data

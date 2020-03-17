from backend import db, repo
from backend.config import API
from backend.general_utils import create_zip, delete_files, parse_img_tag, send_tests_zip
from backend.hooks.delete_utils import delete_criteria, delete_mc_choices, delete_track_route
from backend.mc_choices.utils import format_mc_choice_data
from backend.models import Activity, Card, Checkpoint, Concept, Criteria, Hint, MCChoice, Module, Step, Topic, Track
from backend.tracks.utils import create_tracks_dict
import ast
import os
import requests


# Function to call the Card's Create/Update route
def call_card_routes(card_data, card_name, activity_filename, file):
    # len(card_name) checks if the card is a hard card
    # If it is then you would create a card else you create a hint
    if len(card_name) - 2 < 0:
        card = Card.query.filter_by(filename=card_data["filename"]).first()
        card_data["activity_filename"] = activity_filename

        if card:
            requests.put(API + "/cards", json=card_data)
        else:
            requests.post(API + "/cards", json=card_data)
    else:
        call_hint_routes(card_name, card_data, file)

    return


# Function to all the Criteria Create/Update route
def call_criteria_routes(criteria_data, checkpoint):
    checkpoint_criteria = Criteria.query.filter_by(checkpoint_id=checkpoint.id).all()

    for key, data in criteria_data.items():
        criteria = Criteria.query.filter_by(checkpoint_id=checkpoint.id, criteria_key=key).first()

        data = {
            "criteria_key": key,
            "content": data["content"],
            "checkpoint_id": checkpoint.id
        }

        if criteria:
            requests.put(API + "/criteria", json=data)
            checkpoint_criteria.remove(criteria)
        else:
            requests.post(API + "/criteria", json=data)

    delete_criteria(checkpoint_criteria, checkpoint.id)

    return


# Function to call the Hint Create/Update route
def call_hint_routes(hint_name, hint_data, file):
    hint = Hint.query.filter_by(filename=hint_data["filename"]).first()
    # gets the last element in the list which is the card/hint name
    split_child = hint_data["filename"].split("/")
    hint_path = split_child[-1].split(".")[0]

    parent_length = len(hint_path) - 2
    parent_name = hint_name[:parent_length]
    hint_data["parent_filename"] = "/".join(split_child[:-1]) + "/" + parent_name + ".md"
    hint_data["content"] = md_to_json(file.raw_url)

    if parent_length == 1:
        hint_data["is_card_hint"] = True
    else:
        hint_data["is_card_hint"] = False

    if hint:
        requests.put(API + "/hints", json=hint_data)
    else:
        requests.post(API + "/hints", json=hint_data)

    return


# Function to call the MCChoice's Create/Update route
def call_mc_choice_routes(choice_data, correct_choice, checkpoint_id):
    mc_choices = MCChoice.query.filter_by(checkpoint_id=checkpoint_id).all()
    correct_mc_choice = MCChoice.query.filter_by(correct_checkpoint_id=checkpoint_id,
                                                 choice_key="correct_choice").first()

    if correct_mc_choice:
        mc_choices.append(correct_mc_choice)

    for key, content in choice_data.items():
        mc_choice = MCChoice.query.filter_by(checkpoint_id=checkpoint_id, choice_key=key).first()
        data = format_mc_choice_data(mc_choice, content, key, checkpoint_id)

        if mc_choice:
            mc_choices.remove(mc_choice)
            requests.put(API + "/mc_choices", json=data)
        else:
            requests.post(API + "/mc_choices", json=data)

    data = format_mc_choice_data(correct_mc_choice, correct_choice, "correct_choice", checkpoint_id)

    if correct_mc_choice:
        mc_choices.remove(correct_mc_choice)
        requests.put(API + "/mc_choices", json=data)
    else:
        requests.post(API + "/mc_choices", json=data)
    delete_mc_choices(mc_choices)

    return


# Function to call the Step's Create/Update route
def call_step_routes(step_data, parent_id, parent_type, image_folder):
    for key, data in step_data.items():
        step = None

        if parent_type == "concept":
            step = Step.query.filter_by(concept_id=parent_id, step_key=key).first()
            data["step_key"] = key
            data["concept_id"] = parent_id
            data["image_folder"] = image_folder
            data["type"] = "concept"

        elif parent_type == "hint":
            step = Step.query.filter_by(hint_id=parent_id, step_key=key).first()
            data["step_key"] = key
            data["hint_id"] = parent_id
            data["image_folder"] = image_folder
            data["type"] = "hint"

        if step:
            requests.put(API + "/steps", json=data)
        else:
            requests.post(API + "/steps", json=data)

    return


# Function to call the Topic's Create/Update route
def call_topic_routes(topic_data):
    for key, data in topic_data.items():
        topic = Topic.query.filter_by(github_id=data["github_id"]).first()

        if topic:
            requests.put(API + "/topics", json=data)
        else:
            requests.post(API + "/topics", json=data)

    return


# Function to call the Track's Create/Update route
def call_track_routes(track_data, tracks):
    for key, data in track_data.items():
        track = Track.query.filter_by(github_id=data["github_id"]).first()

        if track:
            requests.put(API + "/tracks", json=data)
            track = Track.query.filter_by(github_id=data["github_id"]).first()
            tracks.pop(track.github_id)
        else:
            requests.post(API + "/tracks", json=data)

    return tracks


# Function to edit the tests.json file
def edit_test_json(file):
    topic_data = {}
    test_file = file.raw_url
    response = requests.get(test_file)
    data = response.text
    track_data = ast.literal_eval(data)

    for key, val in track_data.items():
        for topic in val["topics"]:
            topic_data[topic["name"]] = topic

    parse_tracks(track_data, topic_data)

    return


# Function to get files from all the commits
def get_files(commits):
    files = {}
    deleted_files = {}
    removed_files = []

    for commit in commits:
        change = repo.get_commit(sha=commit["id"])
        removed_files += commit["removed"]

        for file in change.files:
            files[file.filename] = file

    for file in removed_files:
        deleted_files[file] = file

    return files, deleted_files


# Function to parse a markdown file to JSON data
def md_to_json(raw_url):
    response = requests.get(raw_url)
    data = response.text
    f = open("parse.md", "a")
    f.write(data)
    f.close()

    cmd = "md_to_json parse.md"
    output = os.popen(cmd).read()
    result = ast.literal_eval(output)
    os.remove("parse.md")

    return result


# Function to take data from a README.md to Create/Update an activity
def parse_activity(file):
    raw_url = file.raw_url
    data = md_to_json(raw_url)
    data["image"] = parse_img_tag(data["image"], data["image_folder"], "activities")
    data["filename"] = file.filename
    data["github_id"] = int(data["github_id"])
    activity = Activity.query.filter_by(filename=file.filename).first()

    if activity:
        requests.put(API + "/activities", json=data)
    else:
        requests.post(API + "/activities", json=data)

    return data["cards"]


# Function to create/update cards
def parse_card(file, activity_cards, activity_path):
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

    call_card_routes(card_data, card_name, activity_path, file)

    return


# Function to parse checkpoint markdown file
def parse_checkpoint(file):
    data = md_to_json(file.raw_url)
    checkpoint = Checkpoint.query.filter_by(filename=file.filename).first()
    data["filename"] = file.filename

    if checkpoint:
        requests.put(API + "/checkpoints", json=data)
    else:
        requests.post(API + "/checkpoints", json=data)

    return


# Function to take data from a README.md to Create/Update a concept
def parse_concept(file):
    raw_url = file.raw_url
    data = md_to_json(raw_url)
    concept = Concept.query.filter_by(filename=file.filename).first()
    data["filename"] = file.filename

    if concept:
        requests.put(API + "/concepts", json=data)
    else:
        requests.post(API + "/concepts", json=data)

    return


# Function to take data from a README.md to Create/Update a module
def parse_module(file):
    raw_url = file.raw_url
    data = md_to_json(raw_url)
    data = update_module_data(data)
    data["filename"] = file.filename
    module = Module.query.filter_by(filename=file.filename).first()

    if module:
        requests.put(API + "/modules", json=data)
    else:
        requests.post(API + "/modules", json=data)

    return


# Function to take data from a README.md to Create/Update a topic
def parse_topic(file):
    raw_url = file.raw_url
    data = md_to_json(raw_url)
    data = update_topic_data(data, file)
    topic = Topic.query.filter_by(filename=file.filename).first()

    if topic:
        requests.put(API + "/topics", json=data)
    else:
        requests.post(API + "/topics", json=data)

    return


# Function to take the data from tests.json and update it
def parse_tracks(track_data, topic_data):
    tracks = create_tracks_dict()
    tracks = call_track_routes(track_data, tracks)
    delete_track_route(tracks)

    return


# Function to type cast module fields and update image field
def update_module_data(data):
    data["image"] = parse_img_tag(data["image"], data["image_folder"], "modules")

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

from backend import repo
from backend.config import API
from backend.general_utils import clear_white_space, parse_img_tag
from backend.hooks.delete_utils import delete_criteria, delete_mc_choices, delete_steps, delete_track_route
from backend.hooks.update_utils import update_card_data, update_hint_data, update_module_data, update_step_data, \
    update_topic_data
from backend.mc_choices.utils import format_mc_choice_data
from backend.models import Activity, Card, Checkpoint, Concept, Criteria, Hint, MCChoice, Module, Step, Topic, Track
from backend.steps.utils import get_step_from_patent
from backend.tracks.utils import create_tracks_dict
import ast
import os
import requests


# Function to call the Card's Create/Update route
def call_card_routes(card_data, card_name, activity_filename, file):
    # len(card_name) checks if the card is a hard card
    # If it is then you would create a card else you create a hint
    if len(card_name) - 2 <= 0:
        card = Card.query.filter_by(filename=card_data["filename"]).first()
        card_data["activity_filename"] = activity_filename

        if card:
            requests.put(API + "/cards", json=card_data)
        else:
            requests.post(API + "/cards", json=card_data)
    else:
        content = md_to_json(file.raw_url)
        card_data.update(content)
        hint_data = update_hint_data(card_data, card_name)
        call_hint_routes(hint_data)

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
def call_hint_routes(hint_data):
    hint = Hint.query.filter_by(filename=hint_data["filename"]).first()

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
def call_step_routes(data, parent_id, parent_type):
    # Gets all the steps based on the parent
    steps = []
    if parent_type == "concept":
        steps = Step.query.filter_by(concept_id=parent_id).all()
    elif parent_type == "hint":
        steps = Step.query.filter_by(hint_id=parent_id).all()

    for key, step_data in data["steps"].items():
        step_data = update_step_data(step_data, data, key, parent_id, parent_type)
        step = get_step_from_patent(step_data)

        if step:
            requests.put(API + "/steps", json=step_data)
            steps.remove(step)
        else:
            requests.post(API + "/steps", json=step_data)

    delete_steps(steps)

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
    test_file = file.raw_url
    response = requests.get(test_file)
    data = response.text
    track_data = ast.literal_eval(data)
    parse_tracks(track_data)

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
    sanitized_result = clear_white_space(result)
    os.remove("parse.md")

    return sanitized_result


# Function to take data from a README.md to Create/Update an activity
def parse_activity(file):
    data = md_to_json(file.raw_url)
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
    card_data = update_card_data(file, activity_cards)
    call_card_routes(card_data[0], card_data[1], activity_path, file)

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
def parse_tracks(track_data):
    tracks = create_tracks_dict()
    tracks = call_track_routes(track_data, tracks)
    delete_track_route(tracks)

    return

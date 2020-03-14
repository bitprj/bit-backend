from backend import repo
from backend.config import API
from backend.general_utils import create_image_obj
from backend.models import Activity, Card, Checkpoint, Concept, Hint, MCChoice, Module, Step, Topic, Track
from backend.tracks.utils import create_tracks_dict
import ast
import os
import requests


# Function to call the Card's Create/Update route
def call_card_routes(card_data, card_name, activity_filename, file):
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
    checkpoint = Checkpoint.query.get(checkpoint_id)

    for key, content in choice_data.items():
        mc_choice = MCChoice.query.filter_by(checkpoint_id=checkpoint_id, choice_key=key).first()

        data = {
            "content": content,
            "is_correct_choice": False,
            "checkpoint_id": checkpoint_id,
            "choice_key": key
        }

        if mc_choice:
            requests.put(API + "/mc_choices", json=data)
        else:
            requests.post(API + "/mc_choices", json=data)

    mc_choice = MCChoice.query.filter_by(correct_checkpoint_id=checkpoint_id, choice_key="correct_choice").first()

    data = {
        "content": correct_choice,
        "is_correct_choice": True,
        "checkpoint_id": checkpoint_id,
        "choice_key": "correct_choice"
    }

    if mc_choice:
        requests.put(API + "/mc_choices", json=data)
    else:
        requests.post(API + "/mc_choices", json=data)

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


# Function to delete all of the concept's steps
# Need to send the step key and the parent_id which is either concept_id or hint_id
def delete_step_route(steps):
    for step in steps:
        data = {"step_key": step.step_key}

        if step.hint_id:
            data["type"] = "hint"
            data["hint_id"] = step.hint_id
        elif step.concept.id:
            data["type"] = "concept"
            data["concept_id"] = step.concept_id

        requests.delete(API + "/steps", json=data)

    return


# Function to delete MCChoices
def delete_choice_route(choices):
    for choice in choices:
        data = {
            "checkpoint_id": choice.checkpoint_id,
            "choice_key": choice.choice_key
        }
        requests.delete(API + "/choices", json=data)

    return


# Function to call a topic's delete route
def delete_topic_route():
    topics = Topic.query.all()

    # Deletes Topics if they are not associated with a track
    for topic in topics:
        if not topic.tracks:
            data = {
                "github_id": topic.github_id
            }
            requests.delete(API + "/topics", json=data)

    return


# Function to call the track's delete route
def delete_track_route(tracks):
    # Deletes Tracks
    for track in tracks.values():
        requests.delete(API + "/tracks", json=track)

    return


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


# Function to get the raw url of each card
def get_github_urls(folder_path):
    contents = repo.get_contents(path=folder_path)
    cards = {}

    for content in contents:
        if "README.md" not in content.path and "images" not in content.path:
            card_name = content.path.split("/")[2]
            card_name = card_name.split(".")[0]
            cards[card_name] = {
                "raw_url": content.download_url,
                "filename": content.path
            }

    return cards


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
    data["image"] = create_image_obj(data["image"], data["image_folder"], "activities")
    data["filename"] = file.filename
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
    module = Module.query.filter_by(filename=data["filename"]).first()

    if module:
        requests.put(API + "/modules", json=data)
    else:
        requests.post(API + "/modules", json=data)

    return


# Function to take the data from tests.json and update it
def parse_tracks(track_data, topic_data):
    tracks = create_tracks_dict()
    call_topic_routes(topic_data)
    tracks = call_track_routes(track_data, tracks)
    delete_topic_route()
    delete_track_route(tracks)

    return


# Function to type cast module fields and update image field
def update_module_data(data):
    data["image"] = create_image_obj(data["image"], data["image_folder"], "modules")

    if "gems_needed" in data:
        data["gems_needed"] = int(data["gems_needed"])

    return data

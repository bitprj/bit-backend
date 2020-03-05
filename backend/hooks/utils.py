from backend import repo
from backend.config import API
from backend.general_utils import create_image_obj
from backend.models import Activity, Module, Topic, Track
from backend.tracks.utils import create_tracks_dict
import ast
import os
import requests


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
def edit_test_json(files):
    topic_data = {}
    test_file = files["tests.json"].raw_url
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
    removed_files = []

    for commit in commits:
        change = repo.get_commit(sha=commit["id"])
        removed_files += commit["removed"]

        for file in change.files:
            files[file.filename] = file

    return files, removed_files


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
    print(result)
    os.remove("parse.md")

    return result


# Function to take data from a README.md to Create/Update a module
def parse_activity(file):
    raw_url = file.raw_url
    data = md_to_json(raw_url)
    data["image"] = create_image_obj(data, "activities")
    activity = Activity.query.filter_by(github_id=data["github_id"]).first()

    if activity:
        requests.put(API + "/activities", json=data)
    else:
        requests.post(API + "/activities", json=data)

    return


# Function to take data from a README.md to Create/Update a module
def parse_module(file):
    raw_url = file.raw_url
    data = md_to_json(raw_url)
    data = update_module_data(data)
    module = Module.query.filter_by(github_id=data["github_id"]).first()

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
    data["image"] = create_image_obj(data, "modules")

    if "github_id" in data:
        data["github_id"] = int(data["github_id"])

    if "gems_needed" in data:
        data["gems_needed"] = int(data["gems_needed"])

    return data

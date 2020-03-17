from backend import repo
from backend.config import API
from backend.models import Topic
import requests


# Function to delete a Card
def delete_card(file):
    card_name = file.split("/")[-1]
    card_name = card_name.split(".")[0]
    name_length = len(card_name) - 2

    if name_length < 0:
        data = {"filename": file}
        requests.delete(API + "/cards", json=data)
    else:
        data = {"filename": file}
        requests.delete(API + "/hints", json=data)

    return


# Function to delete a Criteria
def delete_criteria(checkpoint_criteria, checkpoint_id):
    for criteria in checkpoint_criteria:
        data = {
            "criteria_key": criteria.criteria_key,
            "checkpoint_id": checkpoint_id
        }
        requests.delete(API + "/criteria", json=data)

    return


# Function to delete files from github
def delete_files(files_to_delete):
    for file in files_to_delete.values():
        if "Checkpoints" in file:
            delete_file(file, "/checkpoints")

        if "Concept" in file:
            delete_file(file, "/concepts")

        if "Module" in file and "Activity" not in file and "README.md" in file:
            delete_file(file, "/modules")

        if "Module" in file and "Activity" in file and "README.md" in file:
            delete_file(file, "/activities")

        if "Module" in file and "Activity" in file and "Cards" in file and file.endswith(".md"):
            delete_card(file)

        if "Topic" in file and "Module" not in file and "Activity" not in file and "README.md" in file:
            delete_file(file, "/topics")

    return


# Function to delete a file depending on its model type
def delete_file(file, model_type):
    data = {"filename": file}
    requests.delete(API + model_type, json=data)

    return


# Function to delete a Criteria
def delete_mc_choices(mc_choices):
    for choice in mc_choices:
        data = {"choice_key": choice.choice_key}

        if choice.correct_checkpoint_id:
            data["is_correct_choice"] = True
            data["checkpoint_id"] = choice.correct_checkpoint_id
        else:
            data["is_correct_choice"] = False
            data["checkpoint_id"] = choice.checkpoint_id

        requests.delete(API + "/mc_choices", json=data)

    return


# Function to call the track's delete route
def delete_track_route(tracks):
    # Deletes Tracks
    for track in tracks.values():
        requests.delete(API + "/tracks", json=track)

    return

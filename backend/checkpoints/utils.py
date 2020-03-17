from backend.general_utils import create_zip, delete_files, parse_img_tag, send_tests_zip
from backend.hooks.utils import call_mc_choice_routes, call_criteria_routes
from backend.models import Card, Checkpoint
import os


# Function to assign a checkpoint to its respective card
def assign_checkpoint_to_card(checkpoint, data):
    checkpoint_path = data["filename"].split("/")[-1]
    card_name = checkpoint_path.split("-")[0] + ".md"
    card_filename = data["cards_folder"] + card_name
    card = Card.query.filter_by(filename=card_filename).first()
    checkpoint.cards.append(card)

    return


# Function to give a checkpoint a test.zip link if the checkpoint is an Autograder checkpoint
def assign_tests_zip_to_checkpoint(checkpoint, test_file_location, filename):
    files = create_zip(test_file_location)
    zip_link = send_tests_zip(filename)
    delete_files(files)
    os.chdir("..")
    checkpoint.tests_zip = zip_link

    return


# Function to choose which checkpoint to create based on type
def create_checkpoint(data):
    checkpoint = Checkpoint(name=data["name"],
                            instruction=data["instruction"],
                            checkpoint_type=data["checkpoint_type"],
                            filename=data["filename"]
                            )
    assign_checkpoint_to_card(checkpoint, data)

    return checkpoint


# Function to edit a checkpoint
def edit_checkpoint(checkpoint, data):
    checkpoint.name = data["name"]
    checkpoint.instruction = data["instruction"]
    checkpoint.checkpoint_type = data["checkpoint_type"]
    checkpoint.filename = data["filename"]
    assign_checkpoint_to_card(checkpoint, data)
    fill_optional_checkpoint_fields(checkpoint, data)

    return


# Function to fill out optional fields in a checkpoint
def fill_optional_checkpoint_fields(checkpoint, data):
    if "image" in data:
        checkpoint.image = parse_img_tag(data["image"], data["image_folder"], "checkpoints")

    if checkpoint.checkpoint_type == "Multiple Choice" and "mc_choices" in data and "correct_choice" in data:
        call_mc_choice_routes(data["mc_choices"], data["correct_choice"], checkpoint.id)

    if checkpoint.checkpoint_type == "Autograder" and "test_file_location" in data:
        checkpoint.test_cases_location = data["test_file_location"]
        assign_tests_zip_to_checkpoint(checkpoint, data["test_file_location"], data["filename"])

    if checkpoint.checkpoint_type == "Video" or checkpoint.checkpoint_type == "Image" and "criteria" in data:
        call_criteria_routes(data["criteria"], checkpoint)

    return

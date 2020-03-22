from backend.general_utils import create_zip, delete_files, parse_img_tag, send_tests_zip
from backend.hooks.utils import call_mc_choice_routes, call_criteria_routes
from backend.models import Activity, Card, Checkpoint
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
    if "github" in os.getcwd():
        os.chdir("..")
    os.chdir("./github")

    files = create_zip(test_file_location)
    zip_link = send_tests_zip(filename)
    delete_files(files)
    checkpoint.tests_zip = zip_link

    return


# Function to choose which checkpoint to create based on type
def create_checkpoint(data):
    checkpoint = Checkpoint(name=data["name"],
                            instruction=data["instruction"],
                            checkpoint_type=data["checkpoint_type"],
                            filename=data["filename"]
                            )

    return checkpoint


# Function to create a command line command for autograder checkpoints
def create_cli_command(checkpoint, files_to_send):
    checkpoint_split = checkpoint.filename.split("/")
    activity_path = "/".join(checkpoint_split[0:3]) + "/README.md"
    activity = Activity.query.filter_by(filename=activity_path).first()
    command_start = "bit_autograder submit -c={} -a={} {}"
    formatted_command = command_start.format(checkpoint.id, activity.id, files_to_send)
    checkpoint.cli_command = formatted_command

    return


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
    # Give a checkpoint and image if there exits an image in data
    if "image" in data:
        checkpoint.image = parse_img_tag(data["image"], data["image_folder"], "checkpoints")

    # If the checkpoint is a multiple choice checkpoint then create choices for the checkpoint
    if checkpoint.checkpoint_type == "Multiple Choice" and "mc_choices" in data and "correct_choice" in data:
        call_mc_choice_routes(data["mc_choices"], data["correct_choice"], checkpoint.id)

    # If the checkpoint is an Autograder checkpoint, create tests.zip file and cli command
    if checkpoint.checkpoint_type == "Autograder" and "test_file_location" in data and "files_to_send" in data:
        checkpoint.test_cases_location = data["test_file_location"]
        assign_tests_zip_to_checkpoint(checkpoint, data["test_file_location"], data["filename"])
        create_cli_command(checkpoint, data["files_to_send"])

    # If there is criteria in the checkpoint then create criteria
    if checkpoint.checkpoint_type == "Video" or checkpoint.checkpoint_type == "Image" and "criteria" in data:
        call_criteria_routes(data["criteria"], checkpoint)

    return

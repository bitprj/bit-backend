from backend.hooks.utils import call_mc_choice_routes
from backend.models import Checkpoint


# Function to choose which checkpoint to create based on type
def create_checkpoint(data):
    checkpoint = Checkpoint(name=data["name"],
                            instruction=data["instruction"],
                            checkpoint_type=data["checkpoint_type"],
                            filename=data["filename"]
                            )

    return checkpoint


# Function to edit a checkpoint
def edit_checkpoint(checkpoint, data):
    checkpoint.name = data["name"]
    checkpoint.instruction = data["instruction"]
    checkpoint.checkpoint_type = data["checkpoint_type"]
    checkpoint.filename = data["filename"]

    if checkpoint.checkpoint_type == "Multiple Choice" and "mc_choices" in data and "correct_choice" in data:
        call_mc_choice_routes(data["mc_choices"], data["correct_choice"], checkpoint.id)

    # if checkpoint.checkpoint_type == "Autograder" and "tests.zip" in data["parameters"]:
    #     test_content_id = data["parameters"]["tests.zip"]["en-US"]["sys"]["id"]
    #     tests = client.asset(test_content_id).fields()["file"]["url"]
    #     checkpoint.tests_zip = tests[2:]

    return

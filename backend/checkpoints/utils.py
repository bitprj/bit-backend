from backend.models import Checkpoint


# Function to choose which checkpoint to create based on type
def create_checkpoint(data):
    checkpoint = Checkpoint(name=data["name"],
                            instruction=data["instruction"],
                            checkpoint_type=data["checkpoint_type"],
                            filename=data["filename"]
                            )

    if checkpoint.checkpoint_type == "Multiple Choice" and "mc_choices" in data["mc_choices"]:
        pass

    return checkpoint


# Function to edit a checkpoint
def edit_checkpoint(checkpoint, data):
    checkpoint.name = data["name"]
    checkpoint.instruction = data["instruction"]
    checkpoint.checkpoint_type = data["checkpoint_type"]
    checkpoint.filename = data["filename"]

    if checkpoint.checkpoint_type == "Multiple Choice" and "mc_choices" in data["mc_choices"]:
        pass
    # if checkpoint.checkpoint_type == "Multiple Choice" and "mc_question" in data["parameters"]:
    #     mc_question = MCQuestion.query.filter_by(
    #         id=data["parameters"]["mc_question"]["en-US"]["sys"]["id"]).first()
    #     checkpoint.mc_question = mc_question
    #
    # if checkpoint.checkpoint_type == "Autograder" and "tests.zip" in data["parameters"]:
    #     test_content_id = data["parameters"]["tests.zip"]["en-US"]["sys"]["id"]
    #     tests = client.asset(test_content_id).fields()["file"]["url"]
    #     checkpoint.tests_zip = tests[2:]

    return

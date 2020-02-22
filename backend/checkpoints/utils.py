from backend import contentful_client
from backend.config import SPACE_ID, CONTENT_DELIVERY_API_KEY
from backend.models import Checkpoint, CheckpointProgress, MCQuestion
from contentful import Client

client = Client(
    SPACE_ID,
    CONTENT_DELIVERY_API_KEY,
    environment='master'
)


# Function to choose which checkpoint to create based on type
def create_checkpoint(contentful_data):
    checkpoint = Checkpoint(contentful_id=contentful_data["entityId"])

    return checkpoint


# Function to create CheckpointProgresses
def create_checkpoint_progresses(cards, student_id):
    checkpoint_progresses = []
    for card in cards:
        if card.checkpoint:
            checkpoint_prog = CheckpointProgress(checkpoint_id=card.checkpoint.id,
                                                 contentful_id=card.checkpoint.contentful_id,
                                                 student_id=student_id
                                                 )
            checkpoint_progresses.append(checkpoint_prog)

    return checkpoint_progresses


# Function to delete a checkpoint from contentful
def delete_checkpoint(checkpoint):
    checkpoint_entry = contentful_client.entries(SPACE_ID, 'master').find(checkpoint.contentful_id)
    checkpoint_entry.unpublish()
    contentful_client.entries(SPACE_ID, 'master').delete(checkpoint.contentful_id)

    return


# Function to edit a checkpoint
def edit_checkpoint(checkpoint, contentful_data):
    checkpoint.name = contentful_data["parameters"]["name"]["en-US"]
    checkpoint.checkpoint_type = contentful_data["parameters"]["checkpointType"]["en-US"]

    if checkpoint.checkpoint_type == "Multiple Choice" and "mc_question" in contentful_data["parameters"]:
        mc_question = MCQuestion.query.filter_by(
            contentful_id=contentful_data["parameters"]["mc_question"]["en-US"]["sys"]["id"]).first()
        checkpoint.mc_question = mc_question

    if checkpoint.checkpoint_type == "Autograder" and "tests.zip" in contentful_data["parameters"]:
        test_content_id = contentful_data["parameters"]["tests.zip"]["en-US"]["sys"]["id"]
        tests = client.asset(test_content_id).fields()["file"]["url"]
        checkpoint.tests_zip = tests[2:]

    return

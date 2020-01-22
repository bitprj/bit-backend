from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Checkpoint, CheckpointProgress


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

    return

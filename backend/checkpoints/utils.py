from backend.models import Checkpoint, CheckpointProgress


# Function to choose which checkpoint to create based on type
def create_checkpoint(contentful_data):
    checkpoint = Checkpoint(contentful_id=contentful_data["entityId"])

    return checkpoint


# Function to create CheckpointProgresses
def create_checkpoint_progresses(checkpoints, student_id):
    print(checkpoints)
    checkpoint_progresses = []

    for checkpoint in checkpoints:
        checkpoint_prog = CheckpointProgress(checkpoint_id=checkpoint.id,
                                             contentful_id=checkpoint.contentful_id,
                                             student_id=student_id
                                             )
        checkpoint_progresses.append(checkpoint_prog)

    return checkpoint_progresses


# Function to edit a checkpoint
def edit_checkpoint(checkpoint, contentful_data):
    checkpoint.name = contentful_data["parameters"]["name"]["en-US"]
    checkpoint.checkpoint_type = contentful_data["parameters"]["checkpointType"]["en-US"]

    return

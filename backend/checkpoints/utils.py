from backend.models import Checkpoint


# Function to choose which checkpoint to create based on type
def create_checkpoint(contentful_data):
    checkpoint = Checkpoint(contentful_id=contentful_data["entityId"])

    return checkpoint


# Function to edit a checkpoint
def edit_checkpoint(checkpoint, contentful_data):
    checkpoint.name = contentful_data["parameters"]["name"]["en-US"]
    checkpoint.checkpoint_type = contentful_data["parameters"]["checkpointType"]["en-US"]

    return


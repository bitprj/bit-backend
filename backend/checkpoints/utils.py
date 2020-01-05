from backend.models import CheckpointImage


# Function to edit a checkpoint
def edit_checkpoint(checkpoint, contentful_data):
    checkpoint.name = contentful_data["parameters"]["name"]["en-US"]

    return


# Function to choose which checkpoint to create based on type
def create_checkpoint(contentful_data):
    checkpoint = None
    checkpoint_type = contentful_data["parameters"]["checkpointType"]["en-US"]

    if checkpoint_type == "Image":
        checkpoint = create_image_checkpoint(contentful_data)

    return checkpoint


# Function to create a CheckpointImage
def create_image_checkpoint(contentful_data):
    checkpoint = CheckpointImage(contentful_id=contentful_data["entityId"],
                                 name=contentful_data["parameters"]["name"]["en-US"],
                                 checkpoint_type=contentful_data["parameters"]["checkpointType"]["en-US"]
                                 )

    return checkpoint

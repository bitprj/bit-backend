from flask import request
from backend import contentful_client
from backend.config import SPACE_ID
from backend.general_utils import add_file


# A function to fill in a checkpoint_progress based on its type
def fill_in_checkpoint_progress(data, checkpoint_prog):
    checkpoint = checkpoint_prog.checkpoint

    if checkpoint.checkpoint_type == "Image":
        image_file = request.files["image"]
        image = add_file(image_file, "checkpoints")
        checkpoint_prog.image_to_receive = image
    elif checkpoint.checkpoint_type == "Video":
        video_file = request.files["video"]
        video = add_file(video_file, "checkpoints")
        checkpoint_prog.video_to_receive = video
    elif checkpoint.checkpoint_type == "Short Answer":
        checkpoint_prog.short_answer_response = data["short_answer_response"]
    elif checkpoint.checkpoint_type == "Multiple Choice":
        checkpoint_prog.multiple_choice_answer = data["multiple_choice_answer"]
        # checkpoint_contentful_id = checkpoint_prog.checkpoint.contentful_id
        # contentful_checkpoint = contentful_client.entries(SPACE_ID, 'master').find(checkpoint_contentful_id)
        # correct_answer_id = contentful_checkpoint.fields()["mc_correct_answer"].to_json()["sys"]
        # print(contentful_checkpoint.fields())
    checkpoint_prog.is_completed = True

    return

from flask import request
from backend.checkpoint_progresses.schemas import autograder_checkpoint_schema, content_progress_schema, \
    mc_checkpoint_schema
from backend.general_utils import add_file


# A function to fill in a checkpoint_progress based on its type
def fill_in_checkpoint_progress(data, checkpoint_prog):
    checkpoint_type = checkpoint_prog.checkpoint.checkpoint_type

    if checkpoint_type == "Image":
        image_file = request.files["content"]
        image = add_file(image_file, "checkpoints")
        checkpoint_prog.content = image
    elif checkpoint_type == "Video":
        video_file = request.files["content"]
        video = add_file(video_file, "checkpoints")
        checkpoint_prog.content = video
    elif checkpoint_type == "Short Answer":
        checkpoint_prog.content = data["content"]
    elif checkpoint_type == "Multiple Choice":
        checkpoint_prog.content = data["content"]
        correct_answer = checkpoint_prog.checkpoint.mc_question.correct_choice

        if data["content"] == correct_answer:
            checkpoint_prog.multiple_choice_is_correct = True
        else:
            checkpoint_prog.multiple_choice_is_correct = False
    checkpoint_prog.is_completed = True

    return


# Function to return a schema based on the checkpoint type
def get_checkpoint_data(checkpoint_prog):
    checkpoint_type = checkpoint_prog.checkpoint.checkpoint_type

    if checkpoint_type == "Multiple Choice":
        return mc_checkpoint_schema
    elif checkpoint_type == "Autograder":
        return autograder_checkpoint_schema
    else:
        return content_progress_schema

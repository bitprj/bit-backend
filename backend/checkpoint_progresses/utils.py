from flask import request
from backend.checkpoint_progresses.schemas import autograder_checkpoint_schema, content_progress_schema, \
    mc_checkpoint_schema
from backend.general_utils import add_file
from backend.models import CheckpointProgress


# Function to create CheckpointProgresses
def create_checkpoint_progresses(cards, student_id):
    checkpoint_progresses = []
    for card in cards:
        if card.checkpoint:
            checkpoint_prog = CheckpointProgress(checkpoint_id=card.checkpoint.id,
                                                 student_id=student_id
                                                 )
            checkpoint_progresses.append(checkpoint_prog)

    return checkpoint_progresses


# A function to fill in a checkpoint_progress based on its type
def fill_in_checkpoint_progress(data, checkpoint_prog):
    checkpoint_type = checkpoint_prog.checkpoint.checkpoint_type

    if checkpoint_type == "Image":
        image_file = request.files["content"]
        image = add_file(image_file, "checkpoints", image_file.filename)
        checkpoint_prog.content = image
    elif checkpoint_type == "Video":
        video_file = request.files["content"]
        video = add_file(video_file, "checkpoints", video_file.filename)
        checkpoint_prog.content = video
    elif checkpoint_type == "Short Answer":
        checkpoint_prog.content = data["content"]
    elif checkpoint_type == "Multiple Choice":
        checkpoint_prog.content = data["content"]
        correct_answer = checkpoint_prog.checkpoint.correct_choice

        if data["content"] == correct_answer:
            checkpoint_prog.multiple_choice_is_correct = True
        else:
            checkpoint_prog.multiple_choice_is_correct = False
    # Marks the checkpoint as complete and fills in the student's comment
    checkpoint_prog.is_completed = True
    checkpoint_prog.student_comment = data["comment"]

    return


# Function to return a schema based on the checkpoint type
def get_checkpoint_data(checkpoint_prog):
    checkpoint_type = checkpoint_prog.checkpoint.checkpoint_type

    if checkpoint_type == "Multiple Choice":
        return mc_checkpoint_schema
    elif checkpoint_type == "Autograder":
        checkpoint_prog.submissions.sort(key=lambda x: x.date_time, reverse=True)
        return autograder_checkpoint_schema
    else:
        return content_progress_schema

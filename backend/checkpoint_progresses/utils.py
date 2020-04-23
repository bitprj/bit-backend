from flask import request
from backend.checkpoint_progresses.schemas import autograder_checkpoint_schema, content_progress_schema, \
    mc_checkpoint_schema
from backend.general_utils import add_file
from backend.models import CheckpointProgress
import json
import uuid


# Function to create CheckpointProgresses
def create_checkpoint_progresses(cards, student_id):
    checkpoint_progresses = []
    for card in cards:
        for checkpoint in card.checkpoints:
            checkpoint_prog = CheckpointProgress(checkpoint_id=checkpoint.id,
                                                 student_id=student_id
                                                 )
            checkpoint_progresses.append(checkpoint_prog)

    return checkpoint_progresses


# A function to fill in a checkpoint_progress based on its type
def fill_in_checkpoint_progress(data, checkpoint_prog):
    checkpoint_type = checkpoint_prog.checkpoint.checkpoint_type

    if checkpoint_type == "Image" or checkpoint_type == "Video":
        file = request.files["content"]
        checkpoint_prog.content = generate_checkpoint_file(file)
        checkpoint_prog.student_comment = data["comment"]
    elif checkpoint_type == "File":
        checkpoint_prog.files = generate_files()
        checkpoint_prog.student_comment = data["comment"]
    elif checkpoint_type == "Short Answer":
        checkpoint_prog.content = data["content"]
    elif checkpoint_type == "Multiple Choice":
        checkpoint_prog.multiple_choice_is_correct = fill_in_mc_checkpoint(checkpoint_prog, data)

    # Marks the checkpoint as complete and fills in the student's comment
    checkpoint_prog.is_completed = True

    return


# Function to fill in the data needed for solving a multiple choice checkpoint
def fill_in_mc_checkpoint(checkpoint_prog, data):
    is_correct = False
    checkpoint_prog.content = data["content"]
    correct_answer = checkpoint_prog.checkpoint.correct_choice.content

    if data["content"] == correct_answer:
        return True

    return is_correct


# Function to generate an image_url based for checkpoints
def generate_checkpoint_file(file):
    unique_str = str(uuid.uuid1())
    unique_str += file.filename
    file_url = add_file(file, "checkpoints", unique_str)

    return file_url


# Function to generate and array of files
def generate_files():
    files = []

    for file in request.files.getlist("content"):
        file_url = json.dumps({"file": generate_checkpoint_file(file)})
        files.append(file_url)

    return files


# Function to return a schema based on the checkpoint type
def get_checkpoint_data(checkpoint_prog):
    checkpoint_type = checkpoint_prog.checkpoint.checkpoint_type

    if checkpoint_type == "Multiple Choice":
        return mc_checkpoint_schema.dump(checkpoint_prog)
    elif checkpoint_type == "Autograder":
        checkpoint_prog.submissions.sort(key=lambda x: x.date_time, reverse=True)
        data = autograder_checkpoint_schema.dump(checkpoint_prog)
        data["content"] = {}
        data["content"]["submissions"] = data["submissions"]
        del data["submissions"]
        return data
    else:
        if checkpoint_prog.checkpoint.checkpoint_type == "File":
            data = content_progress_schema.dump(checkpoint_prog)
            data["content"] = jsonify_checkpoint_files(checkpoint_prog.files)
            return data

        return content_progress_schema.dump(checkpoint_prog)


# Function to jsonfiy the file objects
def jsonify_checkpoint_files(files):
    file_list = []

    for file in files:
        file = json.loads(file)
        file_list.append(file)

    return file_list

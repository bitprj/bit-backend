from flask import request
from backend.general_utils import add_file
import ast


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
    elif checkpoint.checkpoint_type == "okPy":
        test_results = ast.literal_eval(data["JSON_DATA"])
        checkpoint_prog.test_cases_failed = test_results["results"]["num_fail"]
        checkpoint_prog.test_cases_passed = test_results["results"]["num_pass"]

    checkpoint_prog.is_completed = True

    return

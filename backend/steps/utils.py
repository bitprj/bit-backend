from backend.general_utils import create_image_obj
from backend.models import Step


# Function to create a step
def create_step(step_key, step_data, hint_id, image_folder):
    name_length = len(step_data["name"]) - 4
    md_content_length = len(step_data["md_content"]) - 4

    step = Step(name=step_data["name"][4:name_length],
                md_content=step_data["md_content"][3:md_content_length],
                step_key=step_key
                )

    step.hint_id = hint_id
    fill_optional_fields(step, step_data, image_folder)

    return step


# Function to edit a step
def edit_step(step, step_data, image_folder):
    name_length = len(step_data["name"]) - 4
    md_content_length = len(step_data["md_content"]) - 4
    step.name = step_data["name"][4:name_length]
    step.md_content = step_data["md_content"][3:md_content_length]
    fill_optional_fields(step, step_data, image_folder)

    return


# Function to add/update optional step fields
def fill_optional_fields(step, step_data, image_folder):
    if "code_snippet" in step_data:
        step.code_snippet = step_data["code_snippet"]

    if "image" in step_data:
        image = create_image_obj(step_data["image"], image_folder, "steps")
        step.image = image

    return

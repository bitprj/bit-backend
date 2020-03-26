from backend import db
from backend.general_utils import parse_img_tag, send_file_to_cdn
from backend.models import Step
from backend.steps.schemas import step_schema


# Function to create a step
def create_step(step_data):
    # subtract 4 because the content is written in code blocks
    name_length = len(step_data["name"]) - 4
    step = Step(name=step_data["name"][4:name_length],
                step_key=step_data["step_key"]
                )

    if step_data["type"] == "hint":
        step.hint_id = step_data["hint_id"]
    elif step_data["type"] == "concept":
        step.concept_id = step_data["concept_id"]

    fill_optional_fields(step, step_data)

    return step


# Function to delete a list of steps
def delete_steps(steps):
    for step in steps:
        db.session.delete(step)

    return


# Function to edit a step
def edit_step(step, step_data):
    name_length = len(step_data["name"]) - 4
    step.name = step_data["name"][4:name_length]
    fill_optional_fields(step, step_data)
    generate_step_cdn_url(step)

    return


# Function to add/update optional step fields
def fill_optional_fields(step, step_data):
    if "code_snippet" in step_data:
        step.code_snippet = step_data["code_snippet"]

    if "image" in step_data:
        image = parse_img_tag(step_data["image"], step_data["image_folder"], "steps")
        step.image = image

    if "md_content" in step_data:
        md_content_length = len(step_data["md_content"]) - 4
        step.content = step_data["md_content"][3:md_content_length]

    return


# Function to generate the step cdn data
def generate_step_cdn_url(step):
    step_content = step_schema.dump(step)
    filename = None

    if step.hint_id:
        filename = step.hint.filename
    elif step.concept_id:
        filename = step.hint.concept.filename

    parent_path = filename.split("/")
    step_path = "/".join(parent_path[:-1]) + "/steps"
    step_name = step.name.replace(" ", "_")
    step_name += ".json"
    step.content_url = send_file_to_cdn(step_content, step_path, step_name)

    return


# Function to get a step whether its parent is a concept or hint
def get_step_from_patent(data):
    step = None

    if data["type"] == "concept":
        step = Step.query.filter_by(concept_id=data["concept_id"], step_key=data["step_key"]).first()
    elif data["type"] == "hint":
        step = Step.query.filter_by(hint_id=data["hint_id"], step_key=data["step_key"]).first()

    return step

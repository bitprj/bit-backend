from backend import db
from backend.models import Step


# Function to create a step
def create_step(contentful_data):
    step = Step(contentful_data["entityId"]
                )

    return step


# Function to edit a step
def edit_step(step, contentful_data):
    step.heading = contentful_data["parameters"]["heading"]["en-US"]
    # delete_steps(step.steps)
    # step.steps = generate_steps((contentful_data["steps"]))

    return


# Function to create steps
def generate_steps(step_data):
    steps = []

    for step_info in step_data:
        step = create_step(step_info)
        steps.append(step)

    db.session.commit()

    return steps


# Function to delete steps
def delete_steps(steps):
    for step in steps:
        step = Step.query.get(step.id)
        db.session.delete(step)

    db.session.commit()

    return


# Function to validate step data
def validate_step_data(step_data):
    for step_info in step_data:
        error = False
        # error = step_form_schema.validate(step_info)

        if error:
            return error

    return False

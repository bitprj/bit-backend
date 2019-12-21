from backend import db
from backend.models import Step
from backend.steps.schemas import step_form_schema


# Function to create a step
def create_step(step_data):
    step = Step(heading=step_data["heading"],
                content=step_data["content"],
                order=step_data["order"],
                image=step_data["image"]
                )

    db.session.add(step)

    return step


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
        error = step_form_schema.validate(step_info)

        if error:
            return error

    return False

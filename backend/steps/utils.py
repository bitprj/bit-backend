from backend.models import db
from backend.models import Step


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

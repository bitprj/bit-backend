from backend.models import Criteria


# Function to choose which criteria to create based on type
def create_criteria(data):
    criteria = Criteria(content=data["content"],
                        criteria_key=data["criteria_key"],
                        checkpoint_id=data["checkpoint_id"]
                        )

    return criteria


# Function to edit a criteria
def edit_criteria(criteria, data):
    criteria.content = data["content"]
    criteria.criteria_key = data["criteria_key"]

    return

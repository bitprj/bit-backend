from backend.models import MCChoice


# Function to create a mc_choice
def create_mc_choice(contentful_data):
    mc_choice = MCChoice(contentful_data["entityId"])

    return mc_choice


# Function to edit a mc_choice
def edit_mc_choice(mc_choice, contentful_data):
    mc_choice.content = contentful_data["parameters"]["content"]["en-US"]

    return

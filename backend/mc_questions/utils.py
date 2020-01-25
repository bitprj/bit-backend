from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import MCChoice, MCQuestion
from backend.prereqs.fetch import get_mc_choices


# Function to create a mc_question
def create_mc_question(contentful_data):
    mc_question = MCQuestion(contentful_data["entityId"])

    return mc_question


# Function to delete a mc_question's relationship
def delete_mc_question(mc_question):
    # Deletes the mc_question mc_choices in contentful
    for mc_choice in mc_question.mc_choices:
        # Unpublishes the mc_choices first then deletes the mc_choice in contentful
        mc_choice_entry = contentful_client.entries(SPACE_ID, 'master').find(mc_choice.contentful_id)
        mc_choice_entry.unpublish()
        contentful_client.entries(SPACE_ID, 'master').delete(mc_choice.contentful_id)

    return


# Function to edit a mc_question
def edit_mc_question(mc_question, contentful_data):
    choice_id = contentful_data["parameters"]["correct_choice"]["en-US"]["sys"]["id"]
    choice = MCChoice.query.filter_by(contentful_id=choice_id).first()
    mc_question.description = contentful_data["parameters"]["description"]["en-US"]
    mc_question.choices = get_mc_choices((contentful_data["parameters"]["mc_choices"]["en-US"]))
    mc_question.correct_choice = choice

    return

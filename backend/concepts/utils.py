from backend.general_utils import create_schema_json
from backend.hooks.utils import call_step_routes
from backend.models import Concept


# Function to create a concept
def create_concept(data):
    concept = Concept(name=data["concept_name"],
                      filename=data["filename"]
                      )

    return concept


# Function to edit a concept
def edit_concept(concept, data):
    concept.name = data["concept_name"]
    concept.filename = data["filename"]
    call_step_routes(data, concept.id, "concept")
    create_schema_json(concept, "concepts")

    return


# Function to get a list of concepts based on card's filepath
def get_concepts(concepts, card):
    concept_list = []
    card_filepath = card.filename.split("/")
    concept_filepath = card_filepath[0] + "/concepts/"

    for concept in concepts:
        filename = concept_filepath + concept
        target_concept = Concept.query.filter_by(filename=filename).first()

        if target_concept:
            concept_list.append(target_concept)

    return concept_list

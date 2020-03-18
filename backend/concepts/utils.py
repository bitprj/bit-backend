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
    call_step_routes(data["steps"], concept.id, "concept", data["image_folder"])

    return

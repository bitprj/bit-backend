from backend.models import Module
from backend.prereqs.fetch import get_activities
from backend.prereqs.utils import assign_badge_prereqs, delete_badge_prereqs


# Function to create a module
def create_module(form_data):
    module = Module(name=form_data["name"],
                    description=form_data["description"],
                    icon=form_data["icon"]
                    )

    module.activities = get_activities(form_data["activities"])
    module.activity_prereqs = get_activities(form_data["activity_prereqs"])

    return module


# Function to edit a module
def edit_module(module, form_data):
    module.name = form_data["name"]
    module.description = form_data["description"]
    module.icon = form_data["icon"]
    module.activities = get_activities(form_data["activities"])
    module.activity_prereqs = get_activities(form_data["activity_prereqs"])
    delete_badge_prereqs(module)
    assign_badge_prereqs(form_data["badge_prereqs"], module, "Module")

    return

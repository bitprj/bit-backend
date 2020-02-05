from backend import db
from backend.badges.utils import add_badge_weights
from backend.models import Activity, Module
from backend.prereqs.fetch import get_activities
from backend.prereqs.utils import assign_badge_prereqs, delete_badge_prereqs


# Function to create a module
def create_module(contentful_data):
    module = Module(contentful_id=contentful_data["entityId"]
                    )

    return module


# Function to delete badge_weights
def delete_badge_weights(badges):
    for badge in badges:
        db.session.delete(badge)

    db.session.commit()

    return


# Function to edit a module
def edit_module(module, contentful_data):
    module.name = contentful_data["parameters"]["name"]["en-US"]
    module.activities = get_activities(contentful_data["parameters"]["activities"]["en-US"])
    delete_badge_weights(module.badge_weights)
    module.badge_weights = add_badge_weights(contentful_data["parameters"]["badge_weights"]["en-US"], module.id)
    delete_badge_prereqs(module)
    assign_badge_prereqs(contentful_data, module, "Module")

    if "activity_prereqs" in contentful_data["parameters"]:
        module.activity_prereqs = get_activities(contentful_data["parameters"]["activity_prereqs"]["en-US"])

    return


# Function to return a student's current module progress based on the module id
def get_module_progress(student, module_id):
    activities = set(Activity.query.filter(Activity.modules.any(id=module_id)).all())
    completed_activities = set(student.completed_activities).intersection(activities)
    incomplete_activities = set(student.incomplete_activities).intersection(activities)

    activity_progress = {"completed_activities": completed_activities,
                         "incomplete_activities": incomplete_activities
                         }

    return activity_progress

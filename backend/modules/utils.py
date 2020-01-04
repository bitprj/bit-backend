from backend.models import Activity, Module, Student
from backend.prereqs.fetch import get_activities
from backend.prereqs.utils import assign_badge_prereqs, delete_badge_prereqs


# Function to create a module
def create_module(contentful_data):
    module = Module(contentful_id=contentful_data["entityId"]
                    )

    return module


# Function to edit a module
def edit_module(module, contentful_data):
    module.name = contentful_data["parameters"]["name"]["en-US"]
    module.activities = get_activities(contentful_data["parameters"]["activities"]["en-US"])
    delete_badge_prereqs(module)
    assign_badge_prereqs(contentful_data, module, "Module")

    if "activity_prereqs" in contentful_data["parameters"]:
        module.activity_prereqs = get_activities(contentful_data["parameters"]["activity_prereqs"]["en-US"])

    return


# Function to return a student's current module progress based on the module id
def get_module_progress(student_id, module_id):
    student = Student.query.get(student_id)

    activities = set(Activity.query.filter(Activity.modules.any(id=module_id)).all())
    completed_activities = set(student.completed_activities).intersection(activities)
    incomplete_activities = set(student.incomplete_activities).intersection(activities)

    activity_progress = {"completed_activities": completed_activities,
                         "incomplete_activities": incomplete_activities
                         }

    return activity_progress


# Function to check if a module exists in the database
def validate_module(module_id):
    module = Module.query.get(module_id)

    if not module:
        return True

    return False

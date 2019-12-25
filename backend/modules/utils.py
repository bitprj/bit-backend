from backend.models import Activity, Module, Student
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

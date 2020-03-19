from backend import db
# from backend.badges.utils import add_badge_weights
from backend.models import Activity, Module, ModuleProgress, StudentBadges
# from backend.prereqs.fetch import get_activities
# from backend.prereqs.utils import assign_badge_prereqs, delete_badge_prereqs


# Function to create a module
def create_module(data):
    module = Module(filename=data["filename"],
                    name=data["name"],
                    description=data["description"],
                    gems_needed=data["gems_needed"],
                    image=data["image"],
                    github_id=data["github_id"]
                    )

    return module


# Function to add gems to module progress
def add_gems_to_module_progress(student, activity_progress):
    modules_completed = []

    for module in activity_progress.activity.modules:
        if module in student.inprogress_modules:
            module_prog = ModuleProgress.query.filter_by(module_id=module.id,
                                                         student_id=activity_progress.student_id).first()
            if module_prog:
                module_prog.gems += activity_progress.accumulated_gems
                # If the module progress has satisfied the gem requirement added it to the completed module list
                if module_prog.gems >= module_prog.module.gems_needed:
                    modules_completed.append(module_prog)

    return modules_completed


# Function to complete modules. Converts gems from module_progresses to badge xp by weight
def complete_modules(module_progs):
    # Look through each ModuleProgress object
    for prog in module_progs:
        student = prog.student
        # Implements the badge weight and gems to convert to xp
        for badge_prog in prog.module.badge_weights:
            student_badge = StudentBadges.query.filter_by(student_id=prog.student_id,
                                                          badge_id=badge_prog.badge_id).first()
            student_badge.xp += prog.gems * badge_prog.weight
        # Adds module to student's completed list
        student.inprogress_modules.remove(prog.module)
        student.completed_modules.append(prog.module)

    return


# Function to create module progresses
def create_module_progresses(modules, student):
    for module in modules:
        module_prog = ModuleProgress(module_id=module.id,
                                     student_id=student.id,
                                     gems=0)
        student.module_progresses.append(module_prog)

    return


# Function to delete badge_weights
def delete_badge_weights(badges):
    for badge in badges:
        db.session.delete(badge)

    db.session.commit()

    return


# Function to edit a module
def edit_module(module, data):
    module.filename = data["filename"]
    module.name = data["name"]
    module.description = data["description"]
    module.gems_needed = data["gems_needed"]
    module.image = data["image"]

    # module.activities = get_activities(data[
    # delete_badge_weights(module.badge_weights)
    # module.badge_weights = add_badge_weights(contentful_data["parameters"]["badge_weights"]["en-US"], module.id)
    # delete_badge_prereqs(module)
    # assign_badge_prereqs(contentful_data, module, "Module")

    # if "activity_prereqs" in contentful_data["parameters"]:
    #     module.activity_prereqs = get_activities(contentful_data["parameters"]["activity_prereqs"]["en-US"])

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

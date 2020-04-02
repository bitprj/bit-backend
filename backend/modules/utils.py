from backend import db
from backend.general_utils import create_schema_json
# from backend.badges.utils import add_badge_weights
from backend.models import Module, StudentBadges
from backend.module_progresses.utils import can_create_module_progress


# This function is used when a module is added to a classroom
# So the newly added module gets added to the student's incomplete_modules
def add_modules_to_students(modules, students):
    for module in modules:
        for student in students:
            module_prog = can_create_module_progress(student, module)
            db.session.add(module_prog)
            db.session.commit()

    return


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
    module.content_url = create_schema_json(module, "module")

    # delete_badge_weights(module.badge_weights)
    # module.badge_weights = add_badge_weights(contentful_data["parameters"]["badge_weights"]["en-US"], module.id)
    # delete_badge_prereqs(module)
    # assign_badge_prereqs(contentful_data, module, "Module")

    # if "activity_prereqs" in contentful_data["parameters"]:
    #     module.activity_prereqs = get_activities(contentful_data["parameters"]["activity_prereqs"]["en-US"])

    return


# Function to return a list of modules based on the module ids
def get_modules(module_ids):
    modules = []

    for module_id in module_ids:
        module = Module.query.get(module_id)
        modules.append(module)

    return modules

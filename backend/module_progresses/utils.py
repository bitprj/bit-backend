from backend.models import ModuleProgress
from backend.activities.utils import add_activity_to_module_progress


# Function to add gems to module progress
def add_gems_to_module_progress(activity_progress):
    modules_completed = []

    for module in activity_progress.activity.modules:
        module_prog = ModuleProgress.query.filter_by(module_id=module.id,
                                                     student_id=activity_progress.student_id).first()
        if module_prog:
            module_prog.gems += activity_progress.accumulated_gems
            # If the module progress has satisfied the gem requirement added it to the completed module list
            if module_prog.gems >= module_prog.module.gems_needed:
                modules_completed.append(module_prog)

    return modules_completed


# Function to check if a module progress exists, if it does not then create it
# This is usually used to create a ModuleProgress object for a student
def can_create_module_progress(student, module):
    module_prog = ModuleProgress.query.filter_by(student_id=student.id, module_id=module.id).first()

    if not module_prog:
        module_prog = create_module_progress(module, student)
        student.incomplete_modules.append(module)

    return module_prog


# Function to create module progresses
def create_module_progress(module, student):
    module_prog = ModuleProgress(module_id=module.id,
                                 student_id=student.id,
                                 gems=0)

    for activity in module.activities:
        add_activity_to_module_progress(student, activity, module_prog)
    student.module_progresses.append(module_prog)

    return module_prog

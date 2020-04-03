from backend.models import ModuleProgress
from backend.activities.utils import add_activity_to_module_progress


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
        print(module_prog.completed_activities, "c")
        print(module_prog.incomplete_activities, "inc")
        print(module_prog.inprogress_activities, "inp")
    student.module_progresses.append(module_prog)

    return module_prog

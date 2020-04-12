from backend import pusher_client
from backend.models import ActivityProgress, CheckpointProgress, ModuleProgress
from datetime import datetime


# Loops through the checkpoint progresses, finds the checkpoint progress and assigns the comment
def assign_comments(checkpoints, student_id):
    for checkpoint in checkpoints:
        checkpoint_prog = CheckpointProgress.query.filter_by(checkpoint_id=checkpoint["checkpoint_id"],
                                                             student_id=student_id).first()
        checkpoint_prog.teacher_comment = checkpoint["comment"]

    return


# Function to fetch all of the ungraded finished activities in a classroom
def get_activities(students, activities):
    unfiltered_activities = []
    filtered_activities = []

    for student in students:
        student_progs = ActivityProgress.query.filter_by(student_id=student.id, is_completed=True,
                                                         is_graded=False).all()
        unfiltered_activities += student_progs

    for activity_prog in unfiltered_activities:
        if activity_prog.activity in activities:
            filtered_activities.append(activity_prog)

    return unfiltered_activities


# Function to grade a student's activity
# If the user completes the gems requirement for the module, return it
def grade_activity(activity_progress, data):
    student = activity_progress.student
    activity_progress.is_graded = True
    activity_progress.date_graded = datetime.now().date()
    activity_progress.is_passed = pass_activity(data["checkpoints"])
    assign_comments(data["checkpoints"], student.id)

    if activity_progress.is_passed:
        activity_progress.student.global_gems += activity_progress.accumulated_gems
        for module in activity_progress.activity.modules:
            module_prog = ModuleProgress.query.filter_by(module_id=module.id, student_id=student.id).first()
            if activity_progress.activity in module_prog.inprogress_activities:
                module_prog.inprogress_activities.remove(activity_progress.activity)
                module_prog.completed_activities.append(activity_progress.activity)

        if activity_progress.activity in student.current_activities:
            student.current_activities.remove(activity_progress.activity)
            student.completed_activities.append(activity_progress.activity)

    return


# Function to tell if the activity failed or not
def pass_activity(checkpoints):
    for checkpoint in checkpoints:
        if not checkpoint["is_passed"]:
            return False

    return True


# Function to notify a student that their activity has been graded
def pusher_activity(activity_progress):
    data = {
        "activity_name": activity_progress.activity.name,
        "is_passed": activity_progress.is_passed,
        "date_graded": activity_progress.date_graded.strftime('%m/%d/%Y')
    }

    channel_name = activity_progress.student.username + "_activity_feed"
    pusher_client.trigger(channel_name, 'new-record', {'data': data})

    return

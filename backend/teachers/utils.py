from backend import pusher_client
from backend.models import ActivityProgress, CheckpointProgress
from backend.modules.utils import add_gems_to_module_progress
from datetime import datetime


# Loops through the checkpoint progresses, finds the checkpoint progress and assigns the comment
def assign_comments(checkpoints):
    for checkpoint in checkpoints:
        checkpoint_prog = CheckpointProgress.query.get(checkpoint["id"])
        checkpoint_prog.comment = checkpoint["comment"]

    return


# Function to fetch all of the ungraded finished activities in a classroom
def get_activities(classroom):
    ungraded_activities = []

    for student in classroom.students:
        student_activity = ActivityProgress.query.filter_by(student_id=student.id, is_completed=True,
                                                            is_graded=False).first()
        if student_activity:
            ungraded_activities.append(student_activity)

    return ungraded_activities


# Function to grade a student's activity
# If the user completes the gems requirement for the module, return it
def grade_activity(activity_progress, form_data):
    modules_prog_completed = []
    student = activity_progress.student
    assign_comments(form_data["checkpoints_failed"])
    assign_comments(form_data["checkpoints_passed"])

    if form_data["checkpoints_failed"]:
        activity_progress.is_passed = False
    else:
        activity_progress.is_passed = True
        modules_prog_completed = add_gems_to_module_progress(student, activity_progress)

        if activity_progress.activity in student.current_activities:
            student.current_activities.remove(activity_progress.activity)
            student.completed_activities.append(activity_progress.activity)

    activity_progress.is_graded = True
    activity_progress.date_graded = datetime.now().date()

    return modules_prog_completed


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

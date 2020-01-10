from backend import pusher_client
from backend.models import ActivityProgress, CheckpointProgress


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


# Function to notify a student that their activity has been graded
def pusher_activity(activity_progress):
    data = {
        "activity_name": activity_progress.activity.name,
        "is_passed": activity_progress.is_passed,
        "date_graded": activity_progress.date_graded.strftime('%m/%d/%Y')
    }

    print(data)
    channel_name = activity_progress.student.username + "_activity_feed"
    pusher_client.trigger(channel_name, 'new-record', {'data': data})

    return

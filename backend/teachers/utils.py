from backend.models import ActivityProgress, CheckpointProgress


# Function to fetch all of the ungraded finished activities in a classroom
def get_activities(classroom):
    ungraded_activities = []

    for student in classroom.students:
        student_activity = ActivityProgress.query.filter_by(student_id=student.id, is_completed=True).first()
        if student_activity:
            ungraded_activities.append(student_activity)

    return ungraded_activities


# Loops through the checkpoint progresses, finds the checkpoint progress and assigns the comment
def assign_comments(checkpoints):
    for checkpoint in checkpoints:
        checkpoint_prog = CheckpointProgress.query.get(checkpoint["id"])
        checkpoint_prog.comment = checkpoint["comment"]

    return

from backend.models import ActivityProgress


# Function to fetch all of the ungraded finished activities in a classroom
def get_activities(classroom):
    ungraded_activities = []

    for student in classroom.students:
        student_activity = ActivityProgress.query.filter_by(student_id=student.id, is_completed=True).first()
        if student_activity:
            ungraded_activities.append(student_activity)

    return ungraded_activities

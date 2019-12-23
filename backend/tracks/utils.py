from backend.models import Student, Topic, Track
from backend.prereqs.fetch import get_topics


# Function to create a track
def create_track(form_data):
    track = Track(name=form_data["name"],
                  description=form_data["description"],
                  focus=form_data["focus"],
                  topic_num=form_data["topic_num"],
                  image=form_data["image"]
                  )

    track.topics = get_topics(form_data["topics"])
    track.required_topics = get_topics(form_data["required_topics"])

    return track


# Function to edit a track
def edit_track(track, form_data):
    track.name = form_data["name"]
    track.description = form_data["description"]
    track.image = form_data["image"]
    track.topics = get_topics(form_data["topics"])
    track.required_topics = get_topics(form_data["required_topics"])

    return


# Function to return a student's current track progress based on the track_id
def get_track_progress(student_id, track_id):
    student = Student.query.get(student_id)

    topics = set(Topic.query.filter(Topic.tracks.any(id=track_id)).all())
    completed_topics = set(student.completed_topics).intersection(topics)
    incomplete_topics = set(student.incomplete_topics).intersection(topics)
    current_topic = student.topic

    track_progress = {"completed_topics": completed_topics,
                      "incomplete_topics": incomplete_topics,
                      "topic": current_topic}

    return track_progress


# Function to check if a track exists in the database
def validate_track(track_id):
    track = Track.query.get(track_id)

    if not track:
        return True

    return False

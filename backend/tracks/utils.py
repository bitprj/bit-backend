from backend.models import Student, Topic, Track
from backend.prereqs.fetch import get_topics


# Function to create a track
def create_track(contentful_data):
    track = Track(contentful_id=contentful_data["entityId"]
                  )

    return track


# Function to edit an track
def edit_track(track, contentful_data):
    track.name = contentful_data["parameters"]["name"]["en-US"]
    track.topics = get_topics(contentful_data["parameters"]["topics"]["en-US"])

    if "required_topics" in contentful_data["parameters"]:
        track.required_topics = get_topics(contentful_data["parameters"]["required_topics"]["en-US"])

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

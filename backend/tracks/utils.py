from backend.general_utils import send_file_to_cdn, get_topics
from backend.models import Student, Topic, Track
from backend.tracks.schemas import track_schema


# Function to create a track
def create_track(form_data):
    track = Track(github_id=form_data["github_id"],
                  name=form_data["name"],
                  description=form_data["description"]
                  )

    track.topics = get_topics(form_data["topics"])
    # track.required_topics = get_topics(form_data["required_topics"])

    return track


# Function to create a dictionary of Tracks
def create_tracks_dict():
    tracks = {}
    track_list = Track.query.all()

    for track in track_list:
        # Use github_id as key because it is unique
        tracks[track.github_id] = {"github_id": track.github_id}

    return tracks


# Function to edit an track
def edit_track(form_data, track):
    track.name = form_data["name"]
    track.description = form_data["description"]
    track.topics = get_topics(form_data["topics"])
    track_data = track_schema.dump(track)
    send_file_to_cdn(track_data, str(track.id), "tracks", track)
    # track.required_topics = get_topics(form_data["required_topics"])

    return


# Function to return a student's current track progress based on the track_id
def get_track_progress(student_id, track_id):
    student = Student.query.get(student_id)
    topics = set(Topic.query.filter(Topic.tracks.any(id=track_id)).all())
    completed_topics = set(student.completed_topics).intersection(topics)
    incomplete_topics = set(student.incomplete_topics).intersection(topics)

    track_progress = {"completed_topics": completed_topics,
                      "incomplete_topics": incomplete_topics,
                      "inprogress_topics": student.inprogress_topics
                      }

    return track_progress

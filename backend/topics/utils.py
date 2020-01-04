from backend.models import Module, Student, Topic
from backend.prereqs.fetch import get_activities, get_modules
from backend.prereqs.utils import assign_badge_prereqs, delete_badge_prereqs


# Function to create a topic
def create_topic(contentful_data):
    topic = Topic(contentful_id=contentful_data["entityId"]
                  )

    return topic


# Function to delete a topic's relationships
def delete_topic(topic):
    topic.modules = []
    topic.module_prereqs = []
    topic.activity_prereqs = []

    return


# Function to edit an topic
def edit_topic(topic, contentful_data):
    topic.name = contentful_data["parameters"]["name"]["en-US"]
    topic.modules = get_modules(contentful_data["parameters"]["modules"]["en-US"])
    delete_badge_prereqs(topic)
    assign_badge_prereqs(contentful_data, topic, "Topic")

    if "module_prereqs" in contentful_data["parameters"]:
        topic.module_prereqs = get_modules(contentful_data["parameters"]["module_prereqs"]["en-US"])

    if "activity_prereqs" in contentful_data["parameters"]:
        topic.activity_prereqs = get_activities(contentful_data["parameters"]["activity_prereqs"]["en-US"])

    return


# Function to get the student's topic progress based on topic id
def get_topic_progress(student_id, topic_id):
    student = Student.query.get(student_id)
    modules = set(Module.query.filter(Module.topics.any(id=topic_id)).all())
    completed_modules = set(student.completed_modules).intersection(modules)
    incomplete_modules = set(student.incomplete_modules).intersection(modules)

    module_progress = {"completed_modules": completed_modules,
                       "incomplete_modules": incomplete_modules}

    return module_progress


# Function to check if a topic exists in the database
def validate_topic(track_id):
    topic = Topic.query.get(track_id)

    if not topic:
        return True

    return False

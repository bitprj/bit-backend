from backend.general_utils import create_schema_json
from backend.models import Module, Student, Topic
from backend.prereqs.fetch import get_modules


# Function to check if a student has completed the required modules for a topic
def completed_modules(student, modules):
    student_modules = set(student.completed_modules)
    modules_set = set(modules)
    modules_completed = student_modules.intersection(modules_set)

    if modules_completed == modules_set:
        return True

    return False


# Function to create a topic
def create_topic(data):
    topic = Topic(github_id=data["github_id"],
                  name=data["name"],
                  filename=data["filename"],
                  description=data["description"],
                  image=data["image"]
                  )

    if "modules" in data:
        topic.modules = get_modules(data["modules"])

    # if "module_prereqs" in contentful_data["parameters"]:
    #     topic.module_prereqs = get_modules(contentful_data["parameters"]["module_prereqs"]["en-US"])
    #
    # if "activity_prereqs" in contentful_data["parameters"]:
    #     topic.activity_prereqs = get_activities(contentful_data["parameters"]["activity_prereqs"]["en-US"])

    return topic


# Function to delete a topic's relationships
def delete_topic(topic):
    topic.modules = []
    topic.module_prereqs = []
    topic.activity_prereqs = []

    return


# Function to edit an topic
def edit_topic(topic, data):
    topic.name = data["name"]
    topic.description = data["description"]

    if "modules" in data:
        topic.modules = get_modules(data["modules"])
        
    topic.content_url = create_schema_json(topic, "topic")
    # delete_badge_prereqs(topic)
    # assign_badge_prereqs(contentful_data, topic, "Topic")

    # if "module_prereqs" in contentful_data["parameters"]:
    #     topic.module_prereqs = get_modules(contentful_data["parameters"]["module_prereqs"]["en-US"])
    #
    # if "activity_prereqs" in contentful_data["parameters"]:
    #     topic.activity_prereqs = get_activities(contentful_data["parameters"]["activity_prereqs"]["en-US"])

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

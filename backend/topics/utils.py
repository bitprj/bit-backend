from backend.models import Topic
from backend.prereqs.fetch import get_activities, get_modules
from backend.prereqs.utils import assign_badge_prereqs, delete_badge_prereqs


# Function to create a topic
def create_topic(form_data):
    topic = Topic(name=form_data["name"],
                  description=form_data["description"]
                  )

    topic.activity_prereqs = get_activities(form_data["activity_prereqs"])
    topic.modules = get_modules(form_data["modules"])
    topic.module_prereqs = get_modules(form_data["module_prereqs"])

    return topic


# Function to edit a topic
def edit_topic(topic, form_data):
    topic.name = form_data["name"]
    topic.description = form_data["description"]
    topic.activity_prereqs = get_activities(form_data["activity_prereqs"])
    topic.modules = get_modules(form_data["modules"])
    topic.module_prereqs = get_modules(form_data["module_prereqs"])
    delete_badge_prereqs(topic)
    assign_badge_prereqs(form_data["badge_prereqs"], topic, "Topic")

    return

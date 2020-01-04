from backend import db
from backend.models import Badge, ActivityBadgePrereqs, ModuleBadgePrereqs, TopicBadgePrereqs


# Function that creates a badge_reqs depending on the object_type
def assign_badge_prereqs(contentful_data, selected_object, object_type):
    if "badge_prereqs" in contentful_data["parameters"]:
        badge_list = contentful_data["parameters"]["badge_prereqs"]["en-US"]["badge_prereqs"]

        for badge_info in badge_list:
            xp = badge_info["xp"]
            badge = Badge.query.get(badge_info["badge_id"])

            # If the badge exists, then add the badge to the object
            if badge:
                target_badge = None

                if object_type == "Activity":
                    target_badge = ActivityBadgePrereqs(xp=xp)
                    target_badge.badge = badge
                    target_badge.activity_id = selected_object.id
                elif object_type == "Module":
                    target_badge = ModuleBadgePrereqs(xp=xp)
                    target_badge.badge = badge
                    target_badge.module_id = selected_object.id
                elif object_type == "Topic":
                    target_badge = TopicBadgePrereqs(xp=xp)
                    target_badge.badge = badge
                    target_badge.topic_id = selected_object.id

                selected_object.badge_prereqs.append(target_badge)

    return


# Function to add incomplete activities to a student when they choose a track
def assign_incomcomplete_activities(topics):
    activities = []

    for topic in topics:
        for module in topic.modules:
            activities += module.activities

    return activities


# Function to add incomplete modules to a student when they choose a track
def assign_incomplete_modules(topics):
    modules = []

    for topic in topics:
        modules += topic.modules

    return modules


# Function to delete badge prereqs based on the selected object
# selected object could be an Activity, Module
def delete_badge_prereqs(selected_object):
    if selected_object.badge_prereqs:
        for badge in selected_object.badge_prereqs:
            db.session.delete(badge)
        db.session.commit()

    return

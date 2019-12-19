from backend import db
from backend.models import Badge, ActivityBadgePrereqs, TopicBadgePrereqs


# Function that creates a badge_reqs depending on the object_type
def assign_badge_prereqs(badge_data, selected_object, object_type):
    for badge_info in badge_data:
        xp = badge_info["xp"]
        badge = Badge.query.get(badge_info["id"])

        # If the badge exists, then add the badge to the object
        if badge:
            target_badge = None

            if object_type == "Activity":
                target_badge = ActivityBadgePrereqs(xp=xp)
                target_badge.badge = badge
                target_badge.activity_id = selected_object.id
            selected_object.badges.append(target_badge)

    return


# Function to delete badge prereqs
def delete_badge_prereqs(activity):
    for badge in activity.badges:
        db.session.delete(badge)
    db.session.commit()

    return


# Function to create an association object for badges and topics
def create_topic_badge_prereqs(badge_info):
    xp = badge_info["xp"]
    badge = Badge.query.get(badge_info["id"])

    # If the badge exists, then add the badge to the Topic
    if badge:
        topic_badge = TopicBadgePrereqs(xp=xp)
        topic_badge.badge = badge

        return topic_badge

    return


# Function to edit an association object for Topics and Badges
def edit_topic_badge_prereqs(topic, badge_data):
    for badge_info in badge_data:
        badge = Badge.query.get(badge_info["id"])

        if badge:
            target_badge = TopicBadgePrereqs.query.filter_by(topic_id=topic.id, badge_id=badge_info["id"]).first()

            # If the topic already has a badge, edit it
            if target_badge:
                target_badge.xp = badge_info["xp"]
            else:
                # If the topic does not have badge, then create a new one
                topic_badge = create_topic_badge_prereqs(badge_info)
                topic.badges.append(topic_badge)

    return

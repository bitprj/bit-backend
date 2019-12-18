from backend.models import Badge, ActivityBadgePrereqs, TopicBadgePrereqs


# Function to loop through all the badge data and adds the selected badge to an
# Use this when you have an association object with a badge
# def assign_badge_prereqs(selected_object, badge_data, object_type):
#     for badge_info in badge_data:
#         badge_prereq = create_badge_prereqs(badge_info, object_type)
#         selected_object.badges.append(badge_prereq)
#
#     return


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


# Function to create an badge_reqs for Activities
# def create_activity_badge_prereqs(badge_data):
#     for badge_info in badge_data:
#         xp = badge_info["xp"]
#         badge = Badge.query.get(badge_info["id"])
#
#         # If the badge exists, then add the badge to the Activity
#         if badge:
#             activity_badge = ActivityBadgePrereqs(xp=xp)
#             activity_badge.badge = badge
#
#             return activity_badge
#
#     return


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

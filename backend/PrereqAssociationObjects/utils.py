from backend.models import Badge, TopicBadgePrereqs


# Function to loop through all the badge data and adds the selected badge to a topic
def create_topic_badge_loop(topic, badge_data):
    for badge_info in badge_data:
        topic_badge = topic_badge_creation(badge_info)
        topic.badges.append(topic_badge)

    return


# Function to edit an association object for Topics and Badges
def edit_topic_badge_prereqs(topic, badge_data):
    for badge_info in badge_data:
        badge = Badge.query.get(badge_info["id"])

        if badge:
            target_badge = TopicBadgePrereqs.query.filter_by(topic_id=topic.id, badge_id=badge_info["id"]).first()

            # If the topic already has a badge, edit it
            if target_badge:
                print("edit badge")
                target_badge.xp = badge_info["xp"]
            else:
                # If the topic does not have badge, then create a new one
                print("adding new badge")
                topic_badge = topic_badge_creation(badge_info)
                topic.badges.append(topic_badge)

    return


# Function to create an association object for badges and topics
def topic_badge_creation(badge_info):
    xp = badge_info["xp"]
    badge = Badge.query.get(badge_info["id"])

    # If the badge exists, then add the badge to the Topic
    if badge:
        topic_badge = TopicBadgePrereqs(xp=xp)
        topic_badge.badge = badge

        return topic_badge

    return

from backend.models import Badge, TopicBadgePrereqs


# Function to create an association object for Topics and Badges
def create_topic_badge_prereqs(topic, badge_data):
    for badge_info in badge_data:
        xp = badge_info["xp"]
        badge = Badge.query.get(badge_info["id"])

        # If the badge exists, then add the badge to the Topic
        if badge:
            topic_badge = TopicBadgePrereqs(xp=xp)
            topic_badge.badge = badge
            topic.badges.append(topic_badge)

    return

from backend.models import Badge, StudentBadges


# Function to make a list of badges based on contentful_ids
def add_badges(contentful_data):
    badge_list = contentful_data["parameters"]["badges"]["en-US"]
    badges = []

    if badge_list:
        for badge in badge_list:
            contentful_id = badge["sys"]["id"]
            target_badge = Badge.query.filter_by(contentful_id=contentful_id).first()
            badges.append(target_badge)

    return badges

    
# Function to create a badge
def create_badge(contentful_data):
    badge = Badge(contentful_id=contentful_data["entityId"]
                  )

    return badge


# Function to create StudentBadges
def create_student_badges(badges, student_id):
    badge_progresses = []

    for badge in badges:
        if badge.badge:
            badge_prog = StudentBadges(badge_id=badge.badge.id,
                                       contentful_id=badge.badge.contentful_id,
                                       student_id=student_id
                                       )
            badge_progresses.append(badge_prog)

    return badge_progresses


# Function to edit a badge
def edit_badge(badge, contentful_data):
    badge.name = contentful_data["parameters"]["name"]["en-US"]

    return

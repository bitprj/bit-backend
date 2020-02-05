from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Badge, ModuleBadgeWeights, StudentBadges


# Function to make a list of badges based on contentful_ids
def add_badge_weights(badges, module_id):
    badge_list = []

    for badge in badges:
        badge_entry = contentful_client.entries(SPACE_ID, 'master').find(badge["sys"]["id"]).fields()
        target_badge = Badge.query.filter_by(name=badge_entry["badge_name"]).first()
        badge_weight = ModuleBadgeWeights(badge_id=target_badge.id,
                                          module_id=module_id,
                                          weight=badge_entry["weight"])
        badge_list.append(badge_weight)

    return badge_list


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

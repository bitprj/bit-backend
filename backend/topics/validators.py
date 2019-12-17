from backend.models import Badge


# Function to check if a badge exist in the database
def check_badge_existence(badge_data):
    for badge in badge_data:
        target_badge = Badge.query.get(badge["id"])

        # If a badge is None, then return true
        if not target_badge:
            return True

    return False

from backend.models import Badge, Module


# Function to check if the list of module_ids are valid in the database
def validate_modules(module_ids):
    for module_id in module_ids:
        module = Module.query.get(module_id)
        if not module:
            return True

    return False


# Function to check if the list of badge_ids are valid in the database
def validate_badges(badge_data):
    for badge_info in badge_data:
        badge = Badge.query.get(badge_info["id"])

        if not badge:
            return True

    return False

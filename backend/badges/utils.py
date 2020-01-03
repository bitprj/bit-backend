from backend.models import Badge


# Function to create a badge
def create_badge(contentful_data):
    badge = Badge(contentful_id=contentful_data["entityId"]
                  )

    return badge


# Function to edit a badge
def edit_badge(badge, contentful_data):
    badge.name = contentful_data["parameters"]["name"]["en-US"]

    return

from backend.models import Activity


# Function to create a activity
def create_activity(contentful_data):
    activity = Activity(contentful_id=contentful_data["sys"]["id"]
                        )

    return activity


# Function to get an activity based on its contentful id
def get_activity(contentful_data):
    contentful_id = contentful_data["sys"]["id"]
    activity = Activity.query.filter_by(contentful_id=contentful_id).first()

    return activity

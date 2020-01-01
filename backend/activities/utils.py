from backend.models import Activity


# Function to create a activity
def create_activity(contentful_data):
    activity = Activity(contentful_id=contentful_data["entityId"]
                        )

    return activity


# Function to edit an activity
def edit_activity(contentful_data):
    activity = Activity.query.filter_by(contentful_id=contentful_data["entityId"]).first()
    activity.name = contentful_data["parameters"]["name"]["en-US"]

    return


# Function to get an activity based on its contentful id
def get_activity(contentful_data):
    contentful_id = contentful_data["entityId"]
    activity = Activity.query.filter_by(contentful_id=contentful_id).first()

    return activity

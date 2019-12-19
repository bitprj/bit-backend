from backend.models import Activity, Module


# Function to return a list of modules based on a list of module ids
def get_modules(module_ids):
    modules = []

    for module_id in module_ids:
        module = Module.query.get(module_id)
        modules.append(module)

    return modules


# Function to return a list of activities based on a list of activity ids
def get_activities(activity_ids):
    activities = []

    for activity_id in activity_ids:
        activity = Activity.query.get(activity_id)
        activities.append(activity)

    return activities

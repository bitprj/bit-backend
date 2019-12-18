from backend.models import Module


# Function to return a list of modules based on a list of module ids
def get_modules(module_ids):
    modules = []

    for module_id in module_ids:
        module = Module.query.get(module_id)
        modules.append(module)

    return modules

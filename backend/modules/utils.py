from backend.models import Module


# Function to create a module
def create_module(form_data):
    module = Module(name=form_data["name"],
                    description=form_data["description"],
                    icon=form_data["icon"]
                    )

    return module


# Function to edit a module
def edit_module(module, form_data):
    module.name = form_data["name"]
    module.description = form_data["description"]
    module.icon = form_data["icon"]

    return

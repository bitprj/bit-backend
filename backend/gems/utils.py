from backend.models import Gem


# Function to add the gem adjustment amount to the gem variable
def create_gem():
    gem = Gem(amount=0, is_local=False)

    return gem


# Function to edit a gem
def edit_gem(gem, form_data):
    gem_difference = gem.amount + form_data["gem_adjustment"]

    # Only update the gem amount if the gem.amount plus gem_adjustment is greater than 0
    if gem_difference >= 0:
        gem.amount = gem_difference

    return

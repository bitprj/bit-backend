from backend import ma
from backend.badges.schemas import BadgeRequirementSchema
from marshmallow import fields


# This schema is used to validate the module form data
class ModuleFormSchema(ma.Schema):
    name = fields.Str(required=True)
    filename = fields.Str(required=True)
    description = fields.Str(required=True)
    gems_needed = fields.Int(required=True)
    image = fields.Str(required=True)
    image_folder = fields.Str(required=True)
    github_id = fields.Int(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "filename", "description", "gems_needed", "image", "image_folder", "github_id")
        ordered = True


# This schema is used to display data in the Module model
class ModuleSchema(ma.Schema):
    id = fields.Int(required=True)
    content_url = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    gems_needed = fields.Int(required=True)
    # badge_weights = ma.Nested("ModuleBadgeWeightSchema", many=True)
    # badge_prereqs = ma.Nested("BadgeRequirementSchema", many=True)
    # We are referencing another Schema below. You do this in oder to avoid circular referencing
    # The only keyword is used to show the id of the activity
    activities = ma.Nested("ActivitySchema", only=("id",), many=True)

    # activity_prereqs = ma.Nested("ActivitySchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "content_url", "name", "description", "gems_needed", "activities")
        ordered = True


module_form_schema = ModuleFormSchema()
module_schema = ModuleSchema()

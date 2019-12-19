from backend import ma
from backend.badges.schemas import BadgeRequirementSchema
from marshmallow import fields


# This schema is used to validate the activity form data
class ActivityFormSchema(ma.Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    summary = fields.Str(required=True)
    difficulty = fields.Str(required=True)
    image = fields.Str(required=False)
    badge_prereqs = fields.List(fields.Dict(), required=False)
    # module_ids are the list of module_ids that keep track of which modules own this lab
    modules = fields.List(fields.Int(), required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "summary", "difficulty", "image", "badge_prereqs", "module_ids")
        ordered = True


# This schema is used to display data in the Activity model
class ActivitySchema(ma.Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    summary = fields.Str(required=True)
    difficulty = fields.Str(required=True)
    image = fields.Str(required=False)
    badges = ma.Nested(BadgeRequirementSchema, many=True)
    # We are referencing another Schema below. You do this in oder to avoid circular referencing
    # The only keyword is used to show the id of the module
    modules = fields.Nested("ModuleSchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "summary", "difficulty", "image", "badges", "modules")
        ordered = True


activity_form_schema = ActivityFormSchema()
activity_schema = ActivitySchema()

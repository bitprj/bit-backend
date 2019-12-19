from backend import ma
from backend.badges.schemas import BadgeRequirementSchema
from backend.modules.schemas import ModuleSchema
from marshmallow import fields


# This schema is used to validate the activity form data
class ActivityFormSchema(ma.Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    summary = fields.String(required=True)
    difficulty = fields.String(required=True)
    image = fields.Field(required=False)
    badge_prereqs = fields.List(fields.Dict(), required=False)
    # module_ids are the list of module_ids that keep track of which modules own this lab
    modules = fields.List(fields.Int(), required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "summary", "difficulty", "image", "badge_prereqs", "module_ids")
        ordered = True


# This schema is used to display data in the Activity model
class ActivitySchema(ma.Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    summary = fields.String(required=True)
    difficulty = fields.String(required=True)
    image = fields.Field(required=False)
    badges = ma.Nested(BadgeRequirementSchema, many=True)
    modules = ma.Nested(ModuleSchema, many=True)

    class Meta:
        ordered = True


activity_form_schema = ActivityFormSchema()
activity_schema = ActivitySchema()

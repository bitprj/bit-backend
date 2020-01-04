from backend import ma
from backend.badges.schemas import BadgeRequirementSchema
from marshmallow import fields


# This schema is used to validate the module form data
class ModuleFormSchema(ma.Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    icon = fields.Str(required=True)
    badge_prereqs = fields.List(fields.Dict(), required=False)
    activity_prereqs = fields.List(fields.Int(), required=False)
    activities = fields.List(fields.Int(), required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "icon", "badge_prereqs", "activity_prereqs", "activities")
        ordered = True


# This schema is used to display data in the Module model
class ModuleSchema(ma.Schema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)
    badge_prereqs = ma.Nested("BadgeRequirementSchema", many=True)
    # We are referencing another Schema below. You do this in oder to avoid circular referencing
    # The only keyword is used to show the id of the activity
    activities = ma.Nested("ActivitySchema", only=("id",), many=True)
    activity_prereqs = ma.Nested("ActivitySchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "badge_prereqs", "activities", "activity_prereqs")
        ordered = True


# This schema is used to return the module progress
class ModuleProgressSchema(ma.Schema):
    completed_activities = fields.Nested("TopicSchema", only=("id", "name", "description"), many=True)
    incomplete_activities = fields.Nested("TopicSchema", only=("id", "name", "description"), many=True)
    activity = fields.Nested("TopicSchema", only=("id", "name", "description"), missing=None, many=False)

    class Meta:
        # Fields to show when sending data
        fields = ("completed_activities", "incomplete_activities", "activity")
        ordered = True


module_form_schema = ModuleFormSchema()
module_schema = ModuleSchema()
module_progress_schema = ModuleProgressSchema()
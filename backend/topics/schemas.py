from backend import ma
from marshmallow import fields


# This schema is used to validate topic form data
class TopicFormSchema(ma.ModelSchema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    modules = fields.List(fields.Int(), required=False)
    activity_prereqs = fields.List(fields.Int(), required=False)
    module_prereqs = fields.List(fields.Int(), required=False)
    badge_prereqs = fields.List(fields.Dict(), required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "description", "modules", "activity_prereqs", "module_prereqs", "badge_prereqs")
        ordered = True


# This schema is used to keep track
class TopicSchema(ma.ModelSchema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    badge_prereqs = fields.List(fields.Dict(), required=True)
    # Below is just for testing purposes
    # badge_prereqs = fields.Nested("BadgeSchema", required=False, many=True)
    # badges = fields.Nested(BadgeSchema, many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "badge_prereqs")
        ordered = True


topic_schema = TopicSchema()
topic_form_schema = TopicFormSchema()

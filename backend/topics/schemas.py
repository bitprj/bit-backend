from backend import ma
from backend.models import Topic
from marshmallow import fields


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
        model = Topic
        ordered = True


topic_schema = TopicSchema()

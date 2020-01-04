from backend import ma
from backend.badges.schemas import BadgeRequirementSchema
from marshmallow import fields


# This schema is used to display data in the Activity model
class ActivitySchema(ma.Schema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)
    badge_prereqs = ma.Nested(BadgeRequirementSchema, many=True)
    # We are referencing another Schema below. You do this in oder to avoid circular referencing
    cards = fields.Nested("CardSchema", only=("id", "contentful_id"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "badge_prereqs", "cards")
        ordered = True


activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)

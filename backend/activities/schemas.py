from backend import ma
from backend.badges.schemas import BadgeRequirementSchema
from marshmallow import fields


# This schema is used to display data in the Activity model
class ActivitySchema(ma.Schema):
    id = fields.Int(required=True)
    badge_prereqs = ma.Nested(BadgeRequirementSchema, many=True)
    # We are referencing another Schema below. You do this in oder to avoid circular referencing
    # The only keyword is used to show the id of the module and card
    modules = fields.Nested("ModuleSchema", only=("id",), many=True)
    cards = fields.Nested("CardSchema", only=("id", "concepts"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "badge_prereqs", "modules", "cards")
        ordered = True


activity_schema = ActivitySchema()

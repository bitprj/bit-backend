from backend import ma
from marshmallow import fields


# This schema is used to validate the badge form data
class BadgeSchema(ma.Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    threshold = fields.Dict(required=True)
    image = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "threshold", "image")
        ordered = True


# This schema is used to display data in any badge association object
class BadgeRequirementSchema(ma.ModelSchema):
    badge_id = fields.Int(required=False)
    xp = fields.Int(required=False)


badge_schema = BadgeSchema()
badges_schema = BadgeSchema(many=True)

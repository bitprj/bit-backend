from backend import ma
from backend.models import ActivityBadgePrereqs
from marshmallow import fields


class BadgeSchema(ma.Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    threshold = fields.Dict(required=True)
    image = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "threshold", "image")
        ordered = True


class BadgeRequirementSchema(ma.ModelSchema):
    badge_id = fields.Int(required=False)
    xp = fields.Int(required=False)


badge_schema = BadgeSchema()
badges_schema = BadgeSchema(many=True)

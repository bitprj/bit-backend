from backend import ma
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


badge_schema = BadgeSchema()
badges_schema = BadgeSchema(many=True)

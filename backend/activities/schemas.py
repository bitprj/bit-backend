from backend import ma
from marshmallow import fields


class ActivitySchema(ma.Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    summary = fields.String(required=True)
    difficulty = fields.String(required=True)
    image = fields.Field(required=False)
    badge_prereqs = fields.List(fields.Dict, required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "summary", "difficulty", "badge_prereqs", "image")
        ordered = True


class ActivityFileSchema(ma.Schema):
    image = fields.Field(required=True)


activity_schema = ActivitySchema()
activity_file_schema = ActivityFileSchema()

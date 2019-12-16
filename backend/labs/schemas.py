from backend import ma
from marshmallow import fields


class LabSchema(ma.Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    summary = fields.String(required=True)
    difficulty = fields.String(required=True)
    image = fields.Field(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "summary", "difficulty", "image")
        ordered = True


lab_schema = LabSchema()

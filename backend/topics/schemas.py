from backend import ma
from marshmallow import fields


class TrackSchema(ma.Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    badges = fields.List(fields.Dict, required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "badges")
        ordered = True


track_schema = TrackSchema()

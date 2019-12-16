from backend import ma
from marshmallow import fields


class TrackSchema(ma.Schema):
    name = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name")
        ordered = True


track_schema = TrackSchema()

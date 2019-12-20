from backend import ma
from marshmallow import fields


# This schema is used to validate form data for track data
class TrackFormSchema(ma.Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    image = fields.Str(required=True)
    # topics is a list of topic ids
    topics = fields.List(fields.Int(), required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "description", "image", "topics")
        ordered = True


# This schema is used to display track data
class TrackSchema(ma.Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    image = fields.Str(required=True)
    # We are referencing another Schema below. You do this in oder to avoid circular referencing
    # The only keyword is used to show the id of topics
    topics = fields.Nested("TopicSchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "image", "topics")
        ordered = True


track_schema = TrackSchema()
track_form_schema = TrackFormSchema()

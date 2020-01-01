from backend import ma
from marshmallow import fields


# This schema is used to display track data
class TrackSchema(ma.Schema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)
    # We are referencing another Schema below. You do this in oder to avoid circular referencing
    # The only keyword is used to show the id of topics
    topics = fields.Nested("TopicSchema", only=("id",), many=True)
    required_topics = fields.Nested("TopicSchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "topics", "required_topics")
        ordered = True


# This schema is used to return the track progress
class TrackProgressSchema(ma.Schema):
    completed_topics = fields.Nested("TopicSchema", only=("id", "name", "description"), many=True)
    incomplete_topics = fields.Nested("TopicSchema", only=("id", "name", "description"), many=True)
    topic = fields.Nested("TopicSchema", only=("id", "name", "description"), missing=None, many=False)

    class Meta:
        # Fields to show when sending data
        fields = ("completed_topics", "incomplete_topics", "topic")
        ordered = True


track_schema = TrackSchema()
tracks_schema = TrackSchema(many=True)
track_progress_schema = TrackProgressSchema()

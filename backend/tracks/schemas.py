from backend import ma
from marshmallow import fields


# This schema is used to validate form data
class TrackFormSchema(ma.Schema):
    github_id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    topics = fields.List(fields.Int, required=True)
    # required_topics = fields.Nested("TopicSchema", only=("id", "contentful_id"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("github_id", "name", "description", "topics")
        ordered = True


# This schema is used to display track data
class TrackSchema(ma.Schema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=False)
    github_id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    # We are referencing another Schema below. You do this in oder to avoid circular referencing
    # The only keyword is used to show the id of topics
    topics = fields.Nested("TopicSchema", only=("id", "github_id", "name"), many=True)
    # required_topics = fields.Nested("TopicSchema", only=("id", "contentful_id"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "github_id", "name", "description", "topics")
        ordered = True


# This schema is used to return the track progress
class TrackProgressSchema(ma.Schema):
    completed_topics = fields.Nested("TopicSchema", only=("id", "name"), many=True)
    incomplete_topics = fields.Nested("TopicSchema", only=("id", "name"), many=True)
    inprogress_topics = fields.Nested("TopicSchema", only=("id", "name"), many=True)
    topic = fields.Nested("TopicSchema", only=("id", "name"), missing=None, many=False)

    class Meta:
        # Fields to show when sending data
        fields = ("completed_topics", "incomplete_topics", "inprogress_topics", "topic")
        ordered = True


track_schema = TrackSchema()
track_form_schema = TrackFormSchema()
tracks_schema = TrackSchema(many=True)
track_progress_schema = TrackProgressSchema()

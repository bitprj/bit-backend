from backend import ma
from marshmallow import fields


# This schema is used to keep track of checkpoint data
class CheckpointProgressSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    checkpoint_id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    comment = fields.Str(missing=None, required=False)
    is_completed = fields.Boolean(required=True)
    image_to_receive = fields.Str(missing=None, required=False)
    video_to_receive = fields.Str(missing=None, required=False)
    checkpoint = fields.Nested("CheckpointSchema", only=("checkpoint_type",))

    class Meta:
        # Fields to show when sending data
        fields = (
            "id", "checkpoint_id", "contentful_id", "comment", "is_completed", "image_to_receive", "video_to_receive",
            "checkpoint")
        ordered = True


class CheckpointGradingSchema(ma.Schema):
    id = fields.Int(required=True)
    comment = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "comment")
        ordered = True


checkpoint_progress_schema = CheckpointProgressSchema(many=True)

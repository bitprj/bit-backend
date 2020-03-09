from backend import ma
from marshmallow import fields


# This schema is used to display data for an autograder checkpoint
class AutograderCheckpointSchema(ma.ModelSchema):
    submissions = fields.Nested("SubmissionSchema", many=True)
    checkpoint = fields.Nested("CheckpointSchema", only=("checkpoint_type",))

    class Meta:
        # Fields to show when sending data
        fields = ("submissions", "checkpoint")
        ordered = True


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


# This schema is used to display data for Image, Video and Short Answer Checkpoints
class ContentCheckpointSchema(ma.ModelSchema):
    content = fields.Str(required=True)
    checkpoint = fields.Nested("CheckpointSchema", only=("checkpoint_type",))

    class Meta:
        # Fields to show when sending data
        fields = ("content", "checkpoint")
        ordered = True


# This schema is used to display data for a Multiple Choice Checkpoint
class MCCheckpointSchema(ma.ModelSchema):
    content = fields.Str(required=True)
    multiple_choice_is_correct = fields.Bool(required=True)
    checkpoint = fields.Nested("CheckpointSchema", only=("checkpoint_type",))

    class Meta:
        # Fields to show when sending data
        fields = ("content", "multiple_choice_is_correct", "checkpoint")
        ordered = True


# This schema is used to display checkpoint submission data
class SubmissionSchema(ma.ModelSchema):
    results = fields.Field(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("results",)
        ordered = True


autograder_checkpoint_schema = AutograderCheckpointSchema()
checkpoint_progress_schema = CheckpointProgressSchema(many=True)
content_progress_schema = ContentCheckpointSchema()
mc_checkpoint_schema = MCCheckpointSchema()

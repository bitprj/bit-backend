from backend import ma
from marshmallow import fields


# This schema is used to display data for an autograder checkpoint
class AutograderCheckpointSchema(ma.ModelSchema):
    student_comment = fields.Str(required=True)
    checkpoint = fields.Nested("CheckpointSchema", only=("checkpoint_type",))
    submissions = fields.Nested("SubmissionSchema", many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("student_comment", "checkpoint", "submissions")
        ordered = True


# This schema is used to keep track of checkpoint data
class CheckpointProgressSchema(ma.ModelSchema):
    checkpoint_id = fields.Int(required=True)
    student_comment = fields.Str(missing=None, required=False)
    teacher_comment = fields.Str(missing=None, required=False)
    content = fields.Str(required=True)
    is_completed = fields.Boolean(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("checkpoint_id", "student_comment", "teacher_comment", "content", "is_completed")
        ordered = True


class CheckpointGradingSchema(ma.Schema):
    checkpoint_id = fields.Int(required=True)
    is_passed = fields.Bool(required=True)
    comment = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("checkpoint_id", "is_passed", "comment")
        ordered = True


# This schema is used to validate the data in a checkpoint submission
class CheckpointSubmissionSchema(ma.Schema):
    content = fields.Field(required=True)
    comment = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("content", "comment")
        ordered = True


# This schema is used to display data for Image, Video and Short Answer Checkpoints
class ContentCheckpointSchema(ma.ModelSchema):
    content = fields.Str(required=True)
    student_comment = fields.Str(required=True)
    checkpoint = fields.Nested("CheckpointSchema", only=("checkpoint_type",))

    class Meta:
        # Fields to show when sending data
        fields = ("content", "student_comment", "checkpoint")
        ordered = True


# This schema is used to display data for a Multiple Choice Checkpoint
class MCCheckpointSchema(ma.ModelSchema):
    content = fields.Str(required=True)
    student_comment = fields.Str(required=True)
    multiple_choice_is_correct = fields.Bool(required=True)
    checkpoint = fields.Nested("CheckpointSchema", only=("checkpoint_type",))

    class Meta:
        # Fields to show when sending data
        fields = ("content", "student_comment", "multiple_choice_is_correct", "checkpoint")
        ordered = True


# This schema is used to display checkpoint submission data
class SubmissionSchema(ma.ModelSchema):
    results = fields.Field(required=True)
    date_time = fields.DateTime(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("results", "date_time")
        ordered = True


autograder_checkpoint_schema = AutograderCheckpointSchema()
checkpoint_progress_schema = CheckpointProgressSchema(many=True)
checkpoint_submission_schema = CheckpointSubmissionSchema()
content_progress_schema = ContentCheckpointSchema()
mc_checkpoint_schema = MCCheckpointSchema()

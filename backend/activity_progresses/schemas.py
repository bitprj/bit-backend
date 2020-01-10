from backend import ma
from backend.checkpoint_progresses.schemas import CheckpointProgressSchema
from marshmallow import fields


# This schema is used to grade a student's activity
class ActivityProgressGradingSchema(ma.ModelSchema):
    activity_progress_id = fields.Int(required=True)
    checkpoints_failed = fields.Nested("CheckpointGradingSchema", many=True)
    checkpoints_passed = fields.Nested("CheckpointGradingSchema", many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("activity_progress_id", "checkpoints_failed", "checkpoints_passed")
        ordered = True


# This schema is used to display activity progress' checkpoints for the teacher to grade
class ActivityProgressSubmissionSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    student = fields.Nested("StudentSchema", only=("name",), required=True)
    activity = fields.Nested("ActivitySchema", only=("name",), required=True)
    checkpoints = fields.Nested("CheckpointProgressSchema",
                                only=(
                                    "id", "is_completed", "image_to_receive", "video_to_receive",
                                    "checkpoint"),
                                required=True, many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "student", "activity", "checkpoints")
        ordered = True


# This schema is used to display ActivityProgress data
class ActivityProgressSchema(ma.ModelSchema):
    last_card_completed = fields.Int(required=True)
    cards_locked = fields.Nested("CardSchema", only=("id", "contentful_id", "name", "order"), many=True)
    cards_unlocked = fields.Nested("CardSchema", only=("id", "contentful_id", "name", "order"), many=True)
    checkpoints = fields.Nested(CheckpointProgressSchema, only=("checkpoint_id", "contentful_id", "is_completed"),
                                many=True)

    class Meta:
        # Fields to show when sending data
        fields = (
            "last_card_completed", "cards_locked", "cards_unlocked", "checkpoints")
        ordered = True


activity_progress_schema = ActivityProgressSchema()
activity_progress_submission_schema = ActivityProgressSubmissionSchema(many=True)
activity_progress_grading_schema = ActivityProgressGradingSchema()

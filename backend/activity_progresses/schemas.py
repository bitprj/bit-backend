from backend import ma
from marshmallow import fields


# This schema is used to grade a student's activity
class ActivityProgressGradingSchema(ma.ModelSchema):
    student_id = fields.Int(required=True)
    checkpoints = fields.Nested("CheckpointGradingSchema", many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("student_id", "checkpoints")
        ordered = True


# This schema is used to display activity progress' checkpoints for the teacher to grade
class ActivityProgressSubmissionSchema(ma.ModelSchema):
    student = fields.Nested("StudentSchema", only=("name",), required=True)
    checkpoints = fields.Nested("CheckpointProgressSchema", only=("id", "content", "checkpoint"), required=True,
                                many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("student", "checkpoints")
        ordered = True


# This schema is used to display ActivityProgress data
class ActivityProgressSchema(ma.ModelSchema):
    activity = fields.Nested("ActivitySchema", only=("contentful_id",), many=False)

    class Meta:
        # Fields to show when sending data
        fields = (
            "activity",)
        ordered = True


activity_progress_schema = ActivityProgressSchema()
activity_progress_submission_schema = ActivityProgressSubmissionSchema(many=True)
activity_progress_grading_schema = ActivityProgressGradingSchema()

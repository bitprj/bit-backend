from backend import ma
from backend.activities.schemas import ActivityRelSerializer
from backend.checkpoint_progresses.schemas import CheckpointProgressSerializer
from marshmallow import fields
from serpy import IntField, MethodField, Serializer


# This schema is used to grade a student's activity
class ActivityProgressGradingSchema(ma.ModelSchema):
    student_id = fields.Int(required=True)
    checkpoints = fields.Nested("CheckpointGradingSchema", many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("student_id", "checkpoints")
        ordered = True


# The Serpy schema is used to serialize the student's submissions for an Activity
class ActivityProgressSubmissionSerializer(Serializer):
    student_id = IntField(required=True)
    user_id = MethodField("serialized_user_id")
    activity = ActivityRelSerializer()
    checkpoints = MethodField("serialize_checkpoints")

    def serialize_checkpoints(self, activity_prog):
        if not activity_prog:
            return []
        return CheckpointProgressSerializer(activity_prog.checkpoints, many=True).data

    def serialized_user_id(self, actvity_prog):
        if not actvity_prog:
            return None
        return actvity_prog.student.meta.user.id

# This schema is used to display ActivityProgress data
class ActivityProgressSchema(ma.ModelSchema):
    is_completed = fields.Bool(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("is_completed",)
        ordered = True


activity_progress_schema = ActivityProgressSchema()
activity_progress_grading_schema = ActivityProgressGradingSchema()

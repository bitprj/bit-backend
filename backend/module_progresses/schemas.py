from backend import ma
from backend.activities.schemas import ActivityRelSerializer
from marshmallow import fields
from serpy import MethodField, Serializer


class ModuleProgressSerializer(Serializer):
    last_activity_unlocked = ActivityRelSerializer()
    chosen_project = ActivityRelSerializer()
    completed_activities = MethodField("serialize_completed_activities")
    incomplete_activities = MethodField("serialize_incompleted_activities")
    inprogress_activities = MethodField("serialize_inprogress_activities")

    def serialize_completed_activities(self, module_prog):
        if not module_prog.completed_activities:
            return None
        return ActivityRelSerializer(module_prog.completed_activities, many=True).data

    def serialize_incompleted_activities(self, module_prog):
        if not module_prog.incomplete_activities:
            return None
        return ActivityRelSerializer(module_prog.incomplete_activities, many=True).data

    def serialize_inprogress_activities(self, module_prog):
        if not module_prog.inprogress_activities:
            return None
        return ActivityRelSerializer(module_prog.inprogress_activities, many=True).data


# This schema is used to validate data to update ModuleProgress
class ModuleProgressUpdateDataSchema(ma.Schema):
    chosen_project_id = fields.Int(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("chosen_project_id",)
        ordered = True


module_progress_update_data_schema = ModuleProgressUpdateDataSchema()

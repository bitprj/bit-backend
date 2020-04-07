from backend import ma
from backend.activities.schemas import ActivityRelSerializer
from marshmallow import fields
from serpy import MethodField, Serializer


class ModuleProgressSerializer(Serializer):
    last_activity_unlocked = MethodField("serialize_last_activity")
    chosen_project = MethodField("serialize_chosen_project")
    completed_activities = MethodField("serialize_completed_activities")
    incomplete_activities = MethodField("serialize_incompleted_activities")
    inprogress_activities = MethodField("serialize_inprogress_activities")

    def serialize_last_activity(self, module_prog):
        if not module_prog.last_activity_unlocked:
            return None
        return module_prog.last_activity_unlocked.id

    def serialize_chosen_project(self, module_prog):
        if not module_prog.chosen_project:
            return None
        return module_prog.chosen_project.id

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


# This schema is used to return the module progress
class ModuleProgressSchema(ma.Schema):
    last_activity_unlocked = fields.Nested("ActivitySchema", only=("id",), many=False)
    chosen_project = fields.Nested("ActivitySchema", only=("id",), many=False)
    completed_activities = fields.Nested("ActivitySchema", only=("id",), many=True)
    incomplete_activities = fields.Nested("ActivitySchema", only=("id",), many=True)
    inprogress_activities = fields.Nested("ActivitySchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("last_activity_unlocked", "chosen_project", "completed_activities", "incomplete_activities",
                  "inprogress_activities")
        ordered = True


# This schema is used to validate data to update ModuleProgress
class ModuleProgressUpdateDataSchema(ma.Schema):
    chosen_project_id = fields.Int(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("chosen_project_id",)
        ordered = True


module_progress_schema = ModuleProgressSchema()
module_progress_update_data_schema = ModuleProgressUpdateDataSchema()

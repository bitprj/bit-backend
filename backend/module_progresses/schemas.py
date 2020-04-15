from backend import ma
from backend.activities.schemas import ActivityRelSerializer
from marshmallow import fields
from serpy import Serializer


class ModuleProgressSerializer(Serializer):
    last_activity_unlocked = ActivityRelSerializer(required=False)
    chosen_projects = ActivityRelSerializer(many=True, required=False)
    completed_activities = ActivityRelSerializer(many=True, required=False)
    incomplete_activities = ActivityRelSerializer(many=True, required=False)
    inprogress_activities = ActivityRelSerializer(many=True, required=False)


# This schema is used to validate data to update ModuleProgress
class ModuleProgressUpdateDataSchema(ma.Schema):
    chosen_project_ids = fields.List(fields.Int(), required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("chosen_project_ids",)
        ordered = True


module_progress_update_data_schema = ModuleProgressUpdateDataSchema()

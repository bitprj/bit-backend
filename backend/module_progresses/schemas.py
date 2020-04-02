from backend import ma
from marshmallow import fields


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

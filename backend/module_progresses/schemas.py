from backend import ma
from marshmallow import fields


# This schema is used to return the module progress
class ModuleProgressSchema(ma.Schema):
    last_activity_unlocked = fields.Nested("ActivitySchema", only=("id",), many=False)
    chosen_project = fields.Nested("ActivitySchema", only=("id",), many=False)

    class Meta:
        # Fields to show when sending data
        fields = ("last_activity_unlocked", "chosen_project")
        ordered = True


module_progress_schema = ModuleProgressSchema()

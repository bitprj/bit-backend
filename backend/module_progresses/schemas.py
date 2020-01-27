from backend import ma
from marshmallow import fields


# This schema is used to return the module progress
class ModuleProgressSchema(ma.Schema):
    completed_activities = fields.Nested("ActivitySchema", only=("id", "name"), many=True)
    incomplete_activities = fields.Nested("ActivitySchema", only=("id", "name"), many=True)
    activity = fields.Nested("ActivitySchema", only=("id", "name", "description"), missing=None, many=False)

    class Meta:
        # Fields to show when sending data
        fields = ("completed_activities", "incomplete_activities", "activity")
        ordered = True


module_progress_schema = ModuleProgressSchema()
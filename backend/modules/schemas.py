from backend import ma
from marshmallow import fields


class ModuleFormSchema(ma.Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    icon = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "icon")
        ordered = True


class ModuleSchema(ma.Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    icon = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "icon")
        ordered = True


module_form_schema = ModuleFormSchema()
module_schema = ModuleSchema()

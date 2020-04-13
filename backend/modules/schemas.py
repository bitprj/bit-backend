from backend import ma
from backend.badges.schemas import BadgeRequirementSchema
from marshmallow import fields
from serpy import IntField, MethodField, Serializer, StrField


# This schema is used to validate the module form data
class ModuleFormSchema(ma.Schema):
    name = fields.Str(required=True)
    filename = fields.Str(required=True)
    description = fields.Str(required=True)
    gems_needed = fields.Int(required=True)
    image = fields.Str(required=True)
    image_folder = fields.Str(required=True)
    github_id = fields.Int(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "filename", "description", "gems_needed", "image", "image_folder", "github_id")
        ordered = True


# This schema is used to display data in the Module model
class ModuleSchema(ma.Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    gems_needed = fields.Int(required=True)
    activities = ma.Nested("ActivitySchema", only=("id", "is_project"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "gems_needed", "activities")
        ordered = True


# Serpy schema for serialization for module relationships
class ModuleRelSerializer(Serializer):
    id = IntField(required=True)
    name = StrField(required=True)


module_form_schema = ModuleFormSchema()
module_schema = ModuleSchema()

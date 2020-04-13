from backend import ma
from marshmallow import fields, validate
from serpy import IntField, Serializer


# This schema is used to validate the badge form data
class ClassroomFormSchema(ma.Schema):
    name = fields.Str(required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "date_start", "date_end")
        ordered = True


# This schema is used to display the classroom data
class ClassroomSchema(ma.Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    class_code = fields.Str(required=True)
    teacher = fields.Nested("UserSchema", only=("id",))
    students = fields.Nested("UserSchema", only=("id",), many=True)
    modules = fields.Nested("ModuleSchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "date_start", "date_end", "class_code", "teacher", "students", "modules")
        ordered = True


# This schema is used to validate the module_ids when the teacher updates the modules in their classroom
class ClassroomModulesSchema(ma.Schema):
    module_ids = fields.List(fields.Int(), required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("module_ids",)
        ordered = True


# This schema is used to validate a classroom code when a student signs up for a classroom
class ClassroomCodeSchema(ma.Schema):
    class_code = fields.Str(required=True, validate=[validate.Length(min=5, max=5)])

    class Meta:
        # Fields to show when sending data
        fields = ("class_code",)
        ordered = True


# Serpy schema for serialization
class ClassroomSerializer(Serializer):
    id = IntField(required=True)


classroom_code_schema = ClassroomCodeSchema()
classroom_schema = ClassroomSchema()
classroom_form_schema = ClassroomFormSchema()
classroom_modules_schema = ClassroomModulesSchema()

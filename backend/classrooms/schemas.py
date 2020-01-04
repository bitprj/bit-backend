from backend import ma
from marshmallow import fields


# This schema is used to validate the badge form data
class ClassroomFormSchema(ma.Schema):
    name = fields.Str(required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "date_start", "date_end")
        ordered = True


classroom_form_schema = ClassroomFormSchema()

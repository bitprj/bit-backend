from backend import ma
from marshmallow import fields


# This schema is used to validate the concept form data
class ConceptFormSchema(ma.Schema):
    concept_name = fields.Str(required=True)
    image_folder = fields.Str(required=False)
    filename = fields.Str(required=True)
    steps = fields.Dict(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("concept_name", "image_folder", "filename", "steps")
        ordered = True


# This schema is used to keep track
class ConceptSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    filename = fields.Str(required=True)
    steps = fields.Nested("StepSchema", many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "steps")
        ordered = True


concept_form_schema = ConceptFormSchema()
concept_schema = ConceptSchema()

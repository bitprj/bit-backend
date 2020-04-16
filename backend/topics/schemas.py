from backend import ma
from marshmallow import fields
from serpy import IntField, MethodField, Serializer, StrField


# This schema is used to validate form data
class TopicFormSchema(ma.Schema):
    name = fields.Str(required=True)
    filename = fields.Str(required=True)
    description = fields.Str(required=True)
    image = fields.Str(required=True)
    image_folder = fields.Str(required=True)
    modules = fields.List(fields.Str(), required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "filename", "description", "image", "image_folder", "modules")
        ordered = True


# Serpy schema for serialization
class TopicSerializer(Serializer):
    id = IntField(required=True)
    name = StrField(required=True)
    description = StrField(required=True)
    image = StrField(required=True)
    modules = MethodField("module_serializer")

    def module_serializer(self, topic):
        if not topic.modules:
            return []
        return [{"id": module.id} for module in topic.modules]


# Keep this schema for now until we update all models with serpy schemas
# This schema is used to keep track
class TopicSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    image = fields.Str(required=True)
    modules = ma.Nested("ModuleSchema", only=("id", "name"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "modules")
        ordered = True


topic_schema = TopicSchema()
topic_form_schema = TopicFormSchema()

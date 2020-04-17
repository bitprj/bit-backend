from backend import ma
from backend.authors.schemas import AuthorSchema
from backend.cards.schemas import CardSerializer
from backend.models import Activity, Module
from marshmallow import fields, validates, ValidationError
from serpy import BoolField, IntField, MethodField, Serializer, StrField


# This schema is used to validate the activity form data
class ActivityFormSchema(ma.Schema):
    filename = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    summary = fields.Str(required=True)
    difficulty = fields.Str(required=True)
    image = fields.Str(required=True)
    image_folder = fields.Str(required=False)
    cards = fields.Dict(required=True)
    contributors = fields.List(fields.Str(), required=False)
    activity_prerequisites = fields.List(fields.Str(), required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("filename", "name", "description", "summary", "difficulty", "image", "image_folder",
                  "cards", "contributors", "activity_prerequisites")
        ordered = True


# This schema is used to display data in the Activity model
class ActivitySchema(ma.Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    summary = fields.Str(required=True)
    is_project = fields.Bool(required=True)
    image = fields.Str(required=True)
    # We are referencing another Schema below. You do this in oder to avoid circular referencing
    cards = fields.Nested("CardSchema", only=("id",), many=True)
    authors = fields.Nested(AuthorSchema, only=("id", "username"), many=True)
    prerequisite_activities = fields.Nested("ActivitySchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "summary", "is_project", "image", "cards",
                  "authors", "prerequisite_activities")
        ordered = True


# Serpy schema for serialization
class ActivitySerializer(Serializer):
    id = IntField(required=True)
    name = StrField(required=True)
    description = StrField(required=True)
    summary = StrField(required=True)
    difficulty = StrField(required=True)
    image = StrField(required=True)
    is_project = BoolField(required=True)
    cards = MethodField("serialize_cards")
    authors = MethodField("serialize_authors")
    prerequisite_activities = MethodField("serialize_activities")

    def serialize_cards(self, activity):
        if not activity.cards:
            return []
        return CardSerializer(activity.cards, many=True).data

    def serialize_authors(self, activity):
        if not activity.authors:
            return []
        return [{"username": author.username} for author in activity.authors]

    def serialize_activities(self, activity):
        if not activity.prerequisite_activities:
            return []
        return [{"id": activity.id} for activity in activity.prerequisite_activities]


# This is a serpy schema to use for Activity relationships
class ActivityRelSerializer(Serializer):
    id = IntField(required=True)


# This schema is used to display data for a SuggestedActivity
class SuggestedActivitySchema(ma.Schema):
    id = fields.Int(required=True)
    module_id = fields.Int(required=True)

    @validates('id')
    def validate_activity_existence(self, data):
        activity = Activity.query.get(data)

        if not activity:
            raise ValidationError("Activity id does not exist")

    @validates('module_id')
    def validate_activity_existence(self, data):
        module = Module.query.get(data)

        if not module:
            raise ValidationError("Module id does not exist")

    class Meta:
        fields = ("id", "module_id")
        ordered = True


activity_form_schema = ActivityFormSchema()
activity_schema = ActivitySchema()

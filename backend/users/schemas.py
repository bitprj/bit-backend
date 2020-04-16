from backend import ma
from marshmallow import fields
from serpy import IntField, MethodField, Serializer, StrField


# Serpy schema for serialization
class UserSerializer(Serializer):
    id = IntField(required=True)
    name = StrField(required=True)
    email = StrField(required=True)
    github_username = StrField(required=True)
    image = StrField(required=True)
    global_gems = IntField(required=True)
    last_seen = MethodField("serialize_last_seen")

    def serialize_last_seen(self, user):
        if not user.last_seen:
            return None
        return user.last_seen.isoformat()


# This schema is used to display user data,
class UserSchema(ma.Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    roles = fields.Str(required=False)
    image = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "email", "roles", "location", "image")
        ordered = True

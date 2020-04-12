from backend import ma
from marshmallow import fields
from serpy import IntField, MethodField, Serializer


class MetaSerializer(Serializer):
    id = IntField(required=True, label="meta_id")
    user_id = MethodField("serialize_user")
    student_id = MethodField("serialize_student")
    teacher_id = MethodField("serialize_teacher")

    def serialize_user(self, meta):
        if not meta.user:
            return None
        return meta.user.id

    def serialize_student(self, meta):
        if not meta.student:
            return None
        return meta.student.id

    def serialize_teacher(self, meta):
        if not meta.teacher:
            return None
        return meta.teacher.id


# This schema is used to display user data,
class UserSchema(ma.Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    username = fields.Email(required=True)
    location = fields.Str(required=True)
    roles = fields.Str(required=False)
    image = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "username", "roles", "location", "image")
        ordered = True


# This schema is used to validate a Github access token
class ValidAccessTokenSchema(ma.Schema):
    code = fields.Str(required=True)


user_schema = UserSchema()
valid_access_token = ValidAccessTokenSchema()

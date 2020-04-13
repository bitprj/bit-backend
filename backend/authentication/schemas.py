from backend import ma
from marshmallow import fields
from serpy import IntField, MethodField, Serializer, StrField


class MetaSerializer(Serializer):
    id = IntField(required=True, label="meta_id")
    roles = StrField(required=True)
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


# This schema is used to validate a Github access token
class ValidAccessTokenSchema(ma.Schema):
    code = fields.Str(required=True)


valid_access_token = ValidAccessTokenSchema()

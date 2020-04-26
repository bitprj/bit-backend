from backend import ma
from marshmallow import fields


# This schema is used display data for Authors
class AuthorSchema(ma.Schema):
    id = fields.Int(required=True)
    username = fields.Str(required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "username")
        ordered = True


author_schema = AuthorSchema()

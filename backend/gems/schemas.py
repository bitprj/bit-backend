from backend import ma
from marshmallow import fields


class GemSchema(ma.Schema):
    amount = fields.Integer()
    is_local = fields.Boolean()
    gem_adjustment = fields.Integer()

    class Meta:
        # Fields to show when sending data
        fields = ("id", "amount", "is_local", "gem_adjustment")
        ordered = True


gem_schema = GemSchema()

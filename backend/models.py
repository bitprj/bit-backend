from backend import db, ma
from marshmallow import fields
from sqlalchemy.ext.mutable import MutableDict


class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    threshold = db.Column(MutableDict.as_mutable(db.PickleType), nullable=False)
    image = db.Column(db.Text, nullable=False)

    def __init__(self, name, description, threshold, image):
        self.name = name
        self.description = description
        self.threshold = threshold
        self.image = image

    def __repr__(self):
        return f"Badge('{self.name}')"


class BadgeSchema(ma.Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    threshold = fields.Dict(required=True)
    image = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "threshold", "image")


badge_schema = BadgeSchema()
badges_schema = BadgeSchema(many=True)

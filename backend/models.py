from backend import db
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


class Gem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False, default=0)
    is_local = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, amount, is_local):
        self.amount = amount
        self.is_local = is_local

    def __repr__(self):
        return f"Gem('{self.is_local}, {self.amount}')"

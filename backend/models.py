from backend import db
from sqlalchemy.ext.mutable import MutableDict


class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    threshold = db.Column(MutableDict.as_mutable(db.PickleType), nullable=False)
    image = db.Column(db.Text, nullable=False)
    topics = db.relationship("TopicBadgePrereqs", back_populates="badge")

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


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    badge_prereqs = db.relationship("TopicBadgePrereqs", cascade="all,delete", back_populates="topic")

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Track('{self.name}')"


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Track('{self.name}')"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # This id is used so that the user's data like name, and email are not exposed in a jwt token
    public_id = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, unique=True, nullable=False)
    location = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"User('{self.email}')"


class Admin(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __repr__(self):
        return f"Admin('{self.name}')"


class Student(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __repr__(self):
        return f"Student('{self.email}')"


class Teacher(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __repr__(self):
        return f"Teacher('{self.email}')"


################## Association Objects ########################
class TopicBadgePrereqs(db.Model):
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), primary_key=True)
    xp = db.Column(db.Integer, nullable=False)

    badge = db.relationship("Badge", back_populates="topics")
    topic = db.relationship("Topic", back_populates="badge_prereqs")

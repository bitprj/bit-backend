from backend import db
from sqlalchemy.ext.mutable import MutableDict

# This many to many relationship is used to keep track of which activities belong to a module
activity_module_rel = db.Table('activity_module_rel',
                               db.Column('activity_id', db.Integer, db.ForeignKey('activity.id')),
                               db.Column('module_id', db.Integer, db.ForeignKey('module.id'))
                               )

# This many to many relationship is used to keep track of the activities need to access a module
activity_module_prereqs = db.Table('activity_module_prereqs',
                                   db.Column('activity_id', db.Integer, db.ForeignKey('activity.id')),
                                   db.Column('module_id', db.Integer, db.ForeignKey('module.id'))
                                   )


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    # Difficulty can be "Hard", "Medium", "Easy"
    difficulty = db.Column(db.String(40), nullable=False)
    image = db.Column(db.Text, nullable=False)
    # badges keeps track of all the badge xp that are required to an activity
    badges = db.relationship("ActivityBadgePrereqs", cascade="all,delete", back_populates="activity")
    # modules keeps track of all of the modules that an activity belongs to
    module_prereqs = db.relationship('Module', secondary='activity_module_prereqs',
                                     back_populates='activity_prereqs')  # modules keeps track of all of the modules that an activity belongs to
    # modules keeps track of all of the modules that an activity belongs to
    modules = db.relationship('Module', secondary='activity_module_rel', back_populates='activities')

    def __init__(self, name, description, summary, difficulty, image):
        self.name = name
        self.description = description
        self.summary = summary
        self.difficulty = difficulty
        self.image = image

    def __repr__(self):
        return f"Activity('{self.name}')"


class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    threshold = db.Column(MutableDict.as_mutable(db.PickleType), nullable=False)
    image = db.Column(db.Text, nullable=False)
    # activities keep track of all the activities that are related to a badge
    activities = db.relationship("ActivityBadgePrereqs", cascade="all,delete", back_populates="badge")
    # modules keep track of all the modules that are related to a badge
    modules = db.relationship("ModuleBadgePrereqs", cascade="all,delete", back_populates="badge")
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


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.Text, nullable=False)
    # activities keeps track of all of the activities that a module belongs to
    activities = db.relationship('Activity', secondary='activity_module_rel', back_populates='modules')
    # activity_prereqs keeps track of all of the activities that are prereqs to a module
    activity_prereqs = db.relationship('Activity', secondary='activity_module_prereqs', back_populates='module_prereqs')
    # badges is used to keep track of the badge xp perquisite to access the Module
    badges = db.relationship("ModuleBadgePrereqs", cascade="all,delete", back_populates="module")

    def __init__(self, name, description, icon):
        self.name = name
        self.description = description
        self.icon = icon

    def __repr__(self):
        return f"Module('{self.name}')"


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
    name = db.Column(db.Text, nullable=False)
    # username is the email
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, unique=True, nullable=False)
    # Roles are Admin, Teacher, or Student
    roles = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=True)

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def __repr__(self):
        return f"User('{self.username}')"


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
# Association object for labs and badges. This is for prerequisites
class ActivityBadgePrereqs(db.Model):
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), primary_key=True)
    xp = db.Column(db.Integer, nullable=False)
    activity = db.relationship("Activity", back_populates="badges")
    badge = db.relationship("Badge", back_populates="activities")


# Association object for modules and badges. This is for prerequisites
class ModuleBadgePrereqs(db.Model):
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), primary_key=True)
    xp = db.Column(db.Integer, nullable=False)
    module = db.relationship("Module", back_populates="badges")
    badge = db.relationship("Badge", back_populates="modules")


class TopicBadgePrereqs(db.Model):
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), primary_key=True)
    xp = db.Column(db.Integer, nullable=False)

    badge = db.relationship("Badge", back_populates="topics")
    topic = db.relationship("Topic", back_populates="badge_prereqs")

from backend import db
from sqlalchemy.ext.mutable import MutableDict

# RELATIONSHIPS. The below tables are used to keep track of which model belongs with a model
# This many to many relationship is used to keep track of which activities belong to a module and vice versa
activity_module_rel = db.Table('activity_module_rel',
                               db.Column('activity_id', db.Integer, db.ForeignKey('activity.id')),
                               db.Column('module_id', db.Integer, db.ForeignKey('module.id'))
                               )

# This many to many relationship is used to keep track of the modules belong a topic and vice versa
topic_module_rel = db.Table('topic_module_rel',
                            db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
                            db.Column('module_id', db.Integer, db.ForeignKey('module.id'))
                            )

# This many to many relationship is used to keep track of which topics belong to track and vice versa
track_topic_rel = db.Table('track_topic_rel',
                           db.Column('track_id', db.Integer, db.ForeignKey('track.id')),
                           db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'))
                           )

# PREREQUISITE The tables below are used to keep track of which model is a prerequisite to another model
# This many to many relationship is used to keep track of the activities need to access a module
activity_module_prereqs = db.Table('activity_module_prereqs',
                                   db.Column('activity_id', db.Integer, db.ForeignKey('activity.id')),
                                   db.Column('module_id', db.Integer, db.ForeignKey('module.id'))
                                   )

# This many to many relationship is used to keep track of the modules need to access a topic
topic_activity_prereqs = db.Table('topic_activity_prereqs',
                                  db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
                                  db.Column('activity_id', db.Integer, db.ForeignKey('activity.id'))
                                  )

# This many to many relationship is used to keep track of the modules need to access a topic
topic_module_prereqs = db.Table('topic_module_prereqs',
                                db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
                                db.Column('module_id', db.Integer, db.ForeignKey('module.id'))
                                )

# REQUIREMENTS The tables below are used to keep track of which model is a requirement for another model
# This is a many to many relationship to keep track of the required topics that needs to completed
topic_track_reqs = db.Table('track_topic_reqs',
                            db.Column('track_id', db.Integer, db.ForeignKey('track.id')),
                            db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'))
                            )


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    # Difficulty can be "Hard", "Medium", "Easy"
    difficulty = db.Column(db.String(40), nullable=False)
    image = db.Column(db.Text, nullable=False)
    # cards keeps track of all the cards that is owned by an Activity
    cards = db.relationship("Card", cascade="all,delete", back_populates="activity")
    # modules keeps track of all of the modules that an activity belongs to
    modules = db.relationship('Module', secondary='activity_module_rel', back_populates='activities')
    # badge_prereqs keeps track of all the badge xp that are required to an activity
    badge_prereqs = db.relationship("ActivityBadgePrereqs", cascade="all,delete", back_populates="activity")
    # modules keeps track of all of the modules that an activity belongs to
    module_prereqs = db.relationship('Module', secondary='activity_module_prereqs', back_populates='activity_prereqs')
    # topic_prereqs keeps track of the activities that needs to be completed before accessing a topic
    topic_prereqs = db.relationship("Topic", secondary="topic_activity_prereqs", back_populates="activity_prereqs")

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


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    md_file = db.Column(db.Text, nullable=False)
    gems = db.Column(db.Integer, nullable=False)
    # activity_id and activity keeps track of which lab the card is owned by
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"))
    activity = db.relationship("Activity", back_populates="cards")

    def __init__(self, name, md_file, gems, activity_id):
        self.name = name
        self.md_file = md_file
        self.gems = gems
        self.activity_id = activity_id

    def __repr__(self):
        return f"Card('{self.name}')"


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
    # topics keep track of all of the topics that a module belongs to
    topics = db.relationship('Topic', secondary='topic_module_rel', back_populates='modules')
    # activity_prereqs keeps track of all of the activities that are prereqs to a module
    activity_prereqs = db.relationship('Activity', secondary='activity_module_prereqs', back_populates='module_prereqs')
    # badges is used to keep track of the badge xp perquisite to access the Module
    badge_prereqs = db.relationship("ModuleBadgePrereqs", cascade="all,delete", back_populates="module")
    # topic_prereqs is used to keep track of modules that need to be completed before accessing a topic
    topic_prereqs = db.relationship('Topic', secondary='topic_module_prereqs', back_populates='module_prereqs')

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
    # modules keeps track of all of the modules that the belong to a topic
    modules = db.relationship('Module', secondary='topic_module_rel', back_populates='topics')
    # tracks keep track of all of the topics that belong to a track
    tracks = db.relationship("Track", secondary="track_topic_rel", back_populates="topics")
    # activity_prereqs keeps track of the activities needed to access a topic
    activity_prereqs = db.relationship("Activity", secondary="topic_activity_prereqs", back_populates="topic_prereqs")
    # badge_prereqs keeps track of the badge xp needed to access a topic
    badge_prereqs = db.relationship("TopicBadgePrereqs", cascade="all,delete", back_populates="topic")
    # module_prereqs keeps track of the modules needed to access a topic
    module_prereqs = db.relationship('Module', secondary='topic_module_prereqs', back_populates='topic_prereqs')
    # required tracks keep track of the required tracks that need to be completed by the user
    required_tracks = db.relationship("Track", secondary="track_topic_reqs", back_populates="required_topics")

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Track('{self.name}')"


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    focus = db.Column(db.Text, nullable=False)
    # topic num are the number of topics needed to be completed to finish a topic
    topic_num = db.Column(db.Integer, nullable=False)
    image = db.Column(db.Text, nullable=False)
    # topics keep track of which topics belong to a track
    topics = db.relationship("Topic", secondary="track_topic_rel", back_populates="tracks")
    # required topics keep track of the required topics that need to be completed by the user
    required_topics = db.relationship("Topic", secondary="track_topic_reqs", back_populates="required_tracks")

    def __init__(self, name, description, focus, topic_num, image):
        self.name = name
        self.description = description
        self.focus = focus
        self.topic_num = topic_num
        self.image = image

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
    activity = db.relationship("Activity", back_populates="badge_prereqs")
    badge = db.relationship("Badge", back_populates="activities")


# Association object for modules and badges. This is for prerequisites
class ModuleBadgePrereqs(db.Model):
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), primary_key=True)
    xp = db.Column(db.Integer, nullable=False)
    module = db.relationship("Module", back_populates="badge_prereqs")
    badge = db.relationship("Badge", back_populates="modules")


# Association object for topics and badges. This is for prerequisites
class TopicBadgePrereqs(db.Model):
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), primary_key=True)
    xp = db.Column(db.Integer, nullable=False)

    badge = db.relationship("Badge", back_populates="topics")
    topic = db.relationship("Topic", back_populates="badge_prereqs")

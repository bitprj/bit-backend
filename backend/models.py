from backend import db
from sqlalchemy.ext.mutable import MutableDict

# RELATIONSHIPS. The below tables are used to keep track of which model belongs with a model
# This many to many relationship is used to keep track of which activities belong to a module and vice versa
activity_module_rel = db.Table("activity_module_rel",
                               db.Column("activity_id", db.Integer, db.ForeignKey("activity.id")),
                               db.Column("module_id", db.Integer, db.ForeignKey("module.id"))
                               )

# This many to many relationship is used to keep track of which card belongs to a concept and vice versa
card_concept_rel = db.Table("card_concept_rel",
                            db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
                            db.Column("concept_id", db.Integer, db.ForeignKey("concept.id"))
                            )

# This many to many relationship is used to keep track of all of the topics that a student has completed
student_topic_completed_rel = db.Table("student_topic_completed_rel",
                                       db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
                                       db.Column("topic_id", db.Integer, db.ForeignKey("topic.id"))
                                       )

# This many to many relationship is used to keep track of all of the topics that a student has not completed
student_topic_incomplete_rel = db.Table("student_topic_incomplete_rel",
                                        db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
                                        db.Column("track_id", db.Integer, db.ForeignKey("topic.id"))
                                        )

# This many to many relationship is used to keep track of all of the activities that a student has completed
student_activity_completed_rel = db.Table("student_activity_completed_rel",
                                          db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
                                          db.Column("activity_id", db.Integer, db.ForeignKey("activity.id"))
                                          )

# This many to many relationship is used to keep track of all of a student's current activities
student_activity_current_rel = db.Table("student_activity_current_rel",
                                        db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
                                        db.Column("activity_id", db.Integer, db.ForeignKey("activity.id"))
                                        )

# This many to many relationship is used to keep track of all of the activities that a student has not completed
student_activity_incomplete_rel = db.Table("student_activity_incomplete_rel",
                                           db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
                                           db.Column("activity_id", db.Integer, db.ForeignKey("activity.id"))
                                           )

# This many to many relationship is used to keep track of all of the modules that a student has completed
student_module_completed_rel = db.Table("student_module_completed_rel",
                                        db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
                                        db.Column("module_id", db.Integer, db.ForeignKey("module.id"))
                                        )

# This many to many relationship is used to keep track of all of the modules that a student has not completed
student_module_incomplete_rel = db.Table("student_module_incomplete_rel",
                                         db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
                                         db.Column("module_id", db.Integer, db.ForeignKey("module.id"))
                                         )

# This many to many relationship is used to keep track of the modules belong a topic and vice versa
topic_module_rel = db.Table("topic_module_rel",
                            db.Column("topic_id", db.Integer, db.ForeignKey("topic.id")),
                            db.Column("module_id", db.Integer, db.ForeignKey("module.id"))
                            )

# This many to many relationship is used to keep track of which topics belong to track and vice versa
track_topic_rel = db.Table("track_topic_rel",
                           db.Column("track_id", db.Integer, db.ForeignKey("track.id")),
                           db.Column("topic_id", db.Integer, db.ForeignKey("topic.id"))
                           )

# PREREQUISITE The tables below are used to keep track of which model is a prerequisite to another model
# This many to many relationship is used to keep track of the activities need to access a module
activity_module_prereqs = db.Table("activity_module_prereqs",
                                   db.Column("activity_id", db.Integer, db.ForeignKey("activity.id")),
                                   db.Column("module_id", db.Integer, db.ForeignKey("module.id"))
                                   )

# This many to many relationship is used to keep track of the modules need to access a topic
topic_activity_prereqs = db.Table("topic_activity_prereqs",
                                  db.Column("topic_id", db.Integer, db.ForeignKey("topic.id")),
                                  db.Column("activity_id", db.Integer, db.ForeignKey("activity.id"))
                                  )

# This many to many relationship is used to keep track of the modules need to access a topic
topic_module_prereqs = db.Table("topic_module_prereqs",
                                db.Column("topic_id", db.Integer, db.ForeignKey("topic.id")),
                                db.Column("module_id", db.Integer, db.ForeignKey("module.id"))
                                )

# REQUIREMENTS The tables below are used to keep track of which model is a requirement for another model
# This is a many to many relationship to keep track of the required topics that needs to completed
topic_track_reqs = db.Table("track_topic_reqs",
                            db.Column("track_id", db.Integer, db.ForeignKey("track.id")),
                            db.Column("topic_id", db.Integer, db.ForeignKey("topic.id"))
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
    modules = db.relationship("Module", secondary="activity_module_rel", back_populates="activities")
    # badge_prereqs keeps track of all the badge xp that are required to an activity
    badge_prereqs = db.relationship("ActivityBadgePrereqs", cascade="all,delete", back_populates="activity")
    # modules keeps track of all of the modules that an activity belongs to
    module_prereqs = db.relationship("Module", secondary="activity_module_prereqs", back_populates="activity_prereqs")
    # students_completed keeps track of which students have completed an activity
    students_completed = db.relationship("Student", secondary="student_activity_completed_rel",
                                         back_populates="completed_activities")
    # students_incomplete keeps track of the students who have not completed an activity
    students_incomplete = db.relationship("Student", secondary="student_activity_incomplete_rel",
                                          back_populates="incomplete_activities")
    # students_current keeps track of the activities that a student is working on
    students_current = db.relationship("Student", secondary="student_activity_current_rel",
                                       back_populates="current_activities")
    # topic_prereqs keeps track of the activities that needs to be completed before accessing a topic
    topic_prereqs = db.relationship("Topic", secondary="topic_activity_prereqs", back_populates="activity_prereqs")
    # students keep track of the student's activity progress
    students = db.relationship("ActivityProgress", back_populates="student")

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
    # concepts keeps track of which concepts that the card owns
    concepts = db.relationship("Concept", secondary="card_concept_rel", back_populates="cards")
    # hints keep track of the hints that a card owns
    hints = db.relationship("Hint", cascade="all,delete", back_populates="card")

    def __init__(self, name, md_file, gems, activity_id):
        self.name = name
        self.md_file = md_file
        self.gems = gems
        self.activity_id = activity_id

    def __repr__(self):
        return f"Card('{self.name}')"


class Concept(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    # cards keep track of which cards that a concept belongs to
    cards = db.relationship("Card", secondary="card_concept_rel", back_populates="concepts")
    # steps keep track of which steps that a concept owns
    steps = db.relationship("Step", cascade="all,delete", back_populates="concept")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Concept('{self.name}')"


class Gem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False, default=0)
    is_local = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, amount, is_local):
        self.amount = amount
        self.is_local = is_local

    def __repr__(self):
        return f"Gem('{self.is_local}, {self.amount}')"


class Hint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Text, nullable=False)
    # Students spend gems when opening hints
    gems = db.Column(db.Integer, nullable=False)
    # parent refers to the hint that owns a hint
    # if parent is not null then the children are able to be unlocked
    # if parent is null then it is a parent
    # if parent is locked then the hint is unable to be unlocked
    parent = db.Column(db.Integer, nullable=True)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"))
    card = db.relationship("Card", back_populates="hints")
    # steps keep track of which steps a hint owns
    steps = db.relationship("Step", cascade="all,delete", back_populates="hint")

    def __init__(self, name, difficulty, gems, parent):
        self.name = name
        self.difficulty = difficulty
        self.gems = gems
        self.parent = parent

    def __repr__(self):
        return f"Hint('{self.name}')"


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.Text, nullable=False)
    # activities keeps track of all of the activities that a module belongs to
    activities = db.relationship("Activity", secondary="activity_module_rel", back_populates="modules")
    # topics keep track of all of the topics that a module belongs to
    topics = db.relationship("Topic", secondary="topic_module_rel", back_populates="modules")
    # activity_prereqs keeps track of all of the activities that are prereqs to a module
    activity_prereqs = db.relationship("Activity", secondary="activity_module_prereqs", back_populates="module_prereqs")
    # badges is used to keep track of the badge xp perquisite to access the Module
    badge_prereqs = db.relationship("ModuleBadgePrereqs", cascade="all,delete", back_populates="module")
    # topic_prereqs is used to keep track of modules that need to be completed before accessing a topic
    topic_prereqs = db.relationship("Topic", secondary="topic_module_prereqs", back_populates="module_prereqs")
    # students_completed keeps track of which students have completed a module
    students_completed = db.relationship("Student", secondary="student_module_completed_rel",
                                         back_populates="completed_modules")
    # students_incomplete keeps track of the students who have not completed a module
    students_incomplete = db.relationship("Student", secondary="student_module_incomplete_rel",
                                          back_populates="incomplete_modules")

    def __init__(self, name, description, icon):
        self.name = name
        self.description = description
        self.icon = icon

    def __repr__(self):
        return f"Module('{self.name}')"


class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    image = db.Column(db.Text, nullable=False)
    # concept keeps track of concept that a step belongs to
    concept_id = db.Column(db.Integer, db.ForeignKey("concept.id"))
    concept = db.relationship("Concept", back_populates="steps")
    # hint keeps track of a hint that a step belongs to
    hint_id = db.Column(db.Integer, db.ForeignKey("hint.id"))
    hint = db.relationship("Hint", back_populates="steps")

    def __init__(self, heading, content, order, image):
        self.heading = heading
        self.content = content
        self.order = order
        self.image = image

    def __repr__(self):
        return f"Step('{self.heading}')"


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # modules keeps track of all of the modules that the belong to a topic
    modules = db.relationship("Module", secondary="topic_module_rel", back_populates="topics")
    # tracks keep track of all of the topics that belong to a track
    tracks = db.relationship("Track", secondary="track_topic_rel", back_populates="topics")
    # activity_prereqs keeps track of the activities needed to access a topic
    activity_prereqs = db.relationship("Activity", secondary="topic_activity_prereqs", back_populates="topic_prereqs")
    # badge_prereqs keeps track of the badge xp needed to access a topic
    badge_prereqs = db.relationship("TopicBadgePrereqs", cascade="all,delete", back_populates="topic")
    # module_prereqs keeps track of the modules needed to access a topic
    module_prereqs = db.relationship("Module", secondary="topic_module_prereqs", back_populates="topic_prereqs")
    # required tracks keep track of the required tracks that need to be completed by the user
    required_tracks = db.relationship("Track", secondary="track_topic_reqs", back_populates="required_topics")
    # students keep track of the students current topic
    students = db.relationship("Student", back_populates="topic")
    # students_completed keeps track of which students have completed a topic
    students_completed = db.relationship("Student", secondary="student_topic_completed_rel",
                                         back_populates="completed_topics")
    # students_incomplete keeps track of the students who have not completed a topic
    students_incomplete = db.relationship("Student", secondary="student_topic_incomplete_rel",
                                          back_populates="incomplete_topics")

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Topic('{self.name}')"


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
    # students keep track of which student is associated with a particular track
    students = db.relationship("Student", back_populates="current_track")

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
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    def __repr__(self):
        return f"Admin('{self.id}')"


class Student(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    # completed_activities keeps track of all activities that a student has completed
    completed_activities = db.relationship("Activity", secondary="student_activity_completed_rel",
                                           back_populates="students_completed")
    # incomplete_activities keeps track of all the activities that a student has not completed
    incomplete_activities = db.relationship("Activity", secondary="student_activity_incomplete_rel",
                                            back_populates="students_incomplete")
    # current_activities keeps track of all the activities that a student is working on
    current_activities = db.relationship("Activity", secondary="student_activity_current_rel",
                                         back_populates="students_current")
    # completed_modules keeps track of all modules that a student has completed
    completed_modules = db.relationship("Module", secondary="student_module_completed_rel",
                                        back_populates="students_completed")
    # incomplete_topics keeps track of all the modules that a student has not completed
    incomplete_modules = db.relationship("Module", secondary="student_module_incomplete_rel",
                                         back_populates="students_incomplete")
    # completed_topics keeps track of all the topics that a student has completed
    completed_topics = db.relationship("Topic", secondary="student_topic_completed_rel",
                                       back_populates="students_completed")
    # incomplete_topics keeps track of all the topics that a student has not completed
    incomplete_topics = db.relationship("Topic", secondary="student_topic_incomplete_rel",
                                        back_populates="students_incomplete")
    # topic is used to show the students current topic
    current_topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"))
    topic = db.relationship("Topic", back_populates="students")
    # current_track is used to keep track of the student's current track
    current_track_id = db.Column(db.Integer, db.ForeignKey("track.id"))
    current_track = db.relationship("Track", back_populates="students")
    # activity_progresses keeps track of all the progresses that a student has made on their activities
    activity_progresses = db.relationship("ActivityProgress", cascade="all,delete", back_populates="activity")

    def __repr__(self):
        return f"Student('{self.id}')"


class Teacher(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    def __repr__(self):
        return f"Teacher('{self.id}')"


################## Association Objects ########################
# Association object for labs and badges. This is for prerequisites
class ActivityBadgePrereqs(db.Model):
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey("badge.id"), primary_key=True)
    xp = db.Column(db.Integer, nullable=False)
    activity = db.relationship("Activity", back_populates="badge_prereqs")
    badge = db.relationship("Badge", back_populates="activities")


# Association object to keep track of a student's progress in an activity
class ActivityProgress(db.Model):
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    # last_card_completed is last card completed from an activity
    last_card_completed = db.Column(db.Integer, nullable=True)
    submitted_video = db.Column(db.Text, nullable=True)
    grading_is_completed = db.Column(db.Boolean, nullable=True)
    video_is_completed = db.Column(db.Boolean, nullable=True)

    cards_locked = db.relationship("Card", back_populates="activity_locked_cards")
    cards_unlocked = db.relationship("Card", back_populates="activity_unlocked_cards")
    student = db.relationship("Student", back_populates="activity_progresses")
    activity = db.relationship("Activity", back_populates="students")


# Association object for modules and badges. This is for prerequisites
class ModuleBadgePrereqs(db.Model):
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), primary_key=True)
    xp = db.Column(db.Integer, nullable=False)
    module = db.relationship("Module", back_populates="badge_prereqs")
    badge = db.relationship("Badge", back_populates="modules")


# Association object for topics and badges. This is for prerequisites
class TopicBadgePrereqs(db.Model):
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey("badge.id"), primary_key=True)
    xp = db.Column(db.Integer, nullable=False)

    badge = db.relationship("Badge", back_populates="topics")
    topic = db.relationship("Topic", back_populates="badge_prereqs")

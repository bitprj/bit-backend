from backend import db

# RELATIONSHIPS. The below tables are used to keep track of which model belongs with a model
# This many to many relationship is used to keep track of which activities belong to a module and vice versa
activity_module_rel = db.Table("activity_module_rel",
                               db.Column("activity_id", db.Integer, db.ForeignKey("activity.id")),
                               db.Column("module_id", db.Integer, db.ForeignKey("module.id"))
                               )

# This many to many relationship keeps track of the activity progress' failed checkpoints
activity_progress_checkpoint_failed_rel = db.Table("activity_progress_checkpoint_failed_rel",
                                                   db.Column("activity_progress_id", db.Integer,
                                                             db.ForeignKey("activity_progress.id")),
                                                   db.Column("checkpoint_progress_id", db.Integer,
                                                             db.ForeignKey("checkpoint_progress.id"))
                                                   )

# This many to many relationship keeps track of the activity progress' failed checkpoints
activity_progress_checkpoint_passed_rel = db.Table("activity_progress_checkpoint_passed_rel",
                                                   db.Column("activity_progress_id", db.Integer,
                                                             db.ForeignKey("activity_progress.id")),
                                                   db.Column("checkpoint_progress_id", db.Integer,
                                                             db.ForeignKey("checkpoint_progress.id"))
                                                   )

# This many to many relationship keeps track of the activity progress' locked cards
activity_progress_locked_cards_rel = db.Table("activity_progress_locked_cards_rel",
                                              db.Column("activity_progress_id", db.Integer,
                                                        db.ForeignKey("activity_progress.id")),
                                              db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
                                              )

# This many to many relationship keeps track of the activity progress' unlocked cards
activity_progress_unlocked_cards_rel = db.Table("activity_progress_unlocked_cards_rel",
                                                db.Column("activity_progress_id", db.Integer,
                                                          db.ForeignKey("activity_progress.id")),
                                                db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
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
                                        db.Column("topic_id", db.Integer, db.ForeignKey("topic.id"))
                                        )

# This many to many relationship is used to keep track of all of the topics that a student is currently working on
student_topic_inprogress_rel = db.Table("student_topic_inprogress_rel",
                                        db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
                                        db.Column("topic_id", db.Integer, db.ForeignKey("topic.id"))
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

# This many to many relationship is used to keep track of all the classes that a student is in
students_classes_rel = db.Table("student_classes_rel",
                                db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
                                db.Column("classroom_id", db.Integer, db.ForeignKey("classroom.id"))
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
    contentful_id = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=True)
    # cards keeps track of all the cards that is owned by an Activity
    cards = db.relationship("Card", cascade="all,delete", back_populates="activity")
    # checkpoints keep track of all the checkpoints that are owned by an activity
    checkpoints = db.relationship("Checkpoint", cascade="all,delete", back_populates="activity")
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
    students = db.relationship("ActivityProgress", back_populates="activity")

    def __init__(self, contentful_id):
        self.contentful_id = contentful_id

    def __repr__(self):
        return f"Activity('{self.name}')"


class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contentful_id = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=True)
    # activities keep track of all the activities that are related to a badge
    activities = db.relationship("ActivityBadgePrereqs", cascade="all,delete", back_populates="badge")
    # modules keep track of all the modules that are related to a badge
    modules = db.relationship("ModuleBadgePrereqs", cascade="all,delete", back_populates="badge")
    topics = db.relationship("TopicBadgePrereqs", back_populates="badge")

    def __init__(self, contentful_id):
        self.contentful_id = contentful_id

    def __repr__(self):
        return f"Badge('{self.name}')"


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contentful_id = db.Column(db.Text(), nullable=False)
    name = db.Column(db.Text, nullable=True)
    # order is a number to keep track of the order in which this card will be displayed
    order = db.Column(db.Integer, nullable=True)
    # activity_id and activity keeps track of which lab the card is owned by
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"))
    activity = db.relationship("Activity", back_populates="cards")
    # concepts keeps track of which concepts that the card owns
    concepts = db.relationship("Concept", secondary="card_concept_rel", back_populates="cards")
    # hints keep track of the hints that a card owns
    hints = db.relationship("Hint", cascade="all,delete", back_populates="card")
    # activity_locked_cards keep track of all the activities locked cards
    activity_locked_cards = db.relationship("ActivityProgress", secondary="activity_progress_locked_cards_rel",
                                            back_populates="cards_locked")
    # activity_locked_cards keep track of all the activities unlocked cards
    activity_unlocked_cards = db.relationship("ActivityProgress", secondary="activity_progress_unlocked_cards_rel",
                                              back_populates="cards_unlocked")

    def __init__(self, contentful_id):
        self.contentful_id = contentful_id

    def __repr__(self):
        return f"Card('{self.name}')"


class Checkpoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contentful_id = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=True)
    checkpoint_type = db.Column(db.Text, nullable=True)
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"))
    activity = db.relationship("Activity", back_populates="checkpoints")
    activity_progresses = db.relationship("CheckpointProgress", back_populates="checkpoint")

    def __init__(self, contentful_id):
        self.contentful_id = contentful_id

    def __repr__(self):
        return f"Checkpoint('{self.name}')"


class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    class_code = db.Column(db.String(5), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    teacher = db.relationship('Teacher', back_populates='classrooms')
    date_start = db.Column(db.Date)
    date_end = db.Column(db.Date)
    # students keep track of all the students in a classroom
    students = db.relationship('Student', secondary=students_classes_rel, back_populates='classes')

    def __init__(self, name, teacher_id, date_start, date_end):
        self.name = name
        self.teacher_id = teacher_id
        self.date_start = date_start
        self.date_end = date_end

    def __repr__(self):
        return f"Class('{self.name}')"


class Concept(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contentful_id = db.Column(db.Text(), nullable=False)
    name = db.Column(db.Text, nullable=True)
    # cards keep track of which cards that a concept belongs to
    cards = db.relationship("Card", secondary="card_concept_rel", back_populates="concepts")
    # steps keep track of which steps that a concept owns
    steps = db.relationship("Step", cascade="all,delete", back_populates="concept")

    def __init__(self, contentful_id):
        self.contentful_id = contentful_id

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
    contentful_id = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=True)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"))
    card = db.relationship("Card", back_populates="hints")
    parent_hint_id = db.Column(db.Integer, db.ForeignKey("hint.id"), nullable=True)
    hint_children = db.relationship("Hint", cascade="all,delete",
                                    backref=db.backref('parent_hint', remote_side='Hint.id'))
    # steps keep track of which steps a hint owns
    steps = db.relationship("Step", cascade="all,delete", back_populates="hint")
    activity_progresses = db.relationship("HintStatus", back_populates="hint")

    def __init__(self, contentful_id):
        self.contentful_id = contentful_id

    def __repr__(self):
        return f"Hint('{self.name}')"


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contentful_id = db.Column(db.Text(), nullable=False)
    name = db.Column(db.Text, nullable=True)
    # activities keeps track of all of the activities that belongs to a module
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

    def __init__(self, contentful_id):
        self.contentful_id = contentful_id

    def __repr__(self):
        return f"Module('{self.name}')"


class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contentful_id = db.Column(db.Text, nullable=False)
    heading = db.Column(db.Text, nullable=True)
    # concept keeps track of concept that a step belongs to
    concept_id = db.Column(db.Integer, db.ForeignKey("concept.id"))
    concept = db.relationship("Concept", back_populates="steps")
    # hint keeps track of a hint that a step belongs to
    hint_id = db.Column(db.Integer, db.ForeignKey("hint.id"))
    hint = db.relationship("Hint", back_populates="steps")

    def __init__(self, contentful_id):
        self.contentful_id = contentful_id

    def __repr__(self):
        return f"Step('{self.heading}')"


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contentful_id = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=True)
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
    # students_completed keeps track of which students have completed a topic
    students_completed = db.relationship("Student", secondary="student_topic_completed_rel",
                                         back_populates="completed_topics")
    # students_incomplete keeps track of the students who have not completed a topic
    students_incomplete = db.relationship("Student", secondary="student_topic_incomplete_rel",
                                          back_populates="incomplete_topics")
    # students_inprogress keeps track of the students that are currently on a topic
    students_inprogress = db.relationship("Student", secondary="student_topic_inprogress_rel",
                                          back_populates="inprogress_topics")

    def __init__(self, contentful_id):
        self.contentful_id = contentful_id

    def __repr__(self):
        return f"Topic('{self.name}')"


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contentful_id = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=True)
    # topics keep track of which topics belong to a track
    topics = db.relationship("Topic", secondary="track_topic_rel", back_populates="tracks")
    # required topics keep track of the required topics that need to be completed by the user
    required_topics = db.relationship("Topic", secondary="track_topic_reqs", back_populates="required_tracks")
    # students keep track of which student is associated with a particular track
    students = db.relationship("Student", back_populates="current_track")

    def __init__(self, contentful_id):
        self.contentful_id = contentful_id

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
    # inprogress_topics keeps track of all the topics that a student has not completed
    inprogress_topics = db.relationship("Topic", secondary="student_topic_inprogress_rel",
                                        back_populates="students_inprogress")
    # current_track is used to keep track of the student's current track
    current_track_id = db.Column(db.Integer, db.ForeignKey("track.id"))
    current_track = db.relationship("Track", back_populates="students")
    # activity_progresses keeps track of all the progresses that a student has made on their activities
    activity_progresses = db.relationship("ActivityProgress", cascade="all,delete", back_populates="student")
    # classes keeps track of all the student's classes
    classes = db.relationship("Classroom", secondary=students_classes_rel, back_populates="students")

    def __repr__(self):
        return f"Student('{self.id}')"


class Teacher(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    classrooms = db.relationship('Classroom', back_populates='teacher')

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
    id = db.Column('id', db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    is_graded = db.Column(db.Boolean, nullable=False, default=False)
    is_passed = db.Column(db.Boolean, nullable=False, default=False)
    # last_card_completed is last card completed from an activity
    last_card_completed = db.Column(db.Integer, nullable=True)
    date_graded = db.Column(db.Date, nullable=True)

    # cards_locked keeps track os the progresses' locked cards
    cards_locked = db.relationship("Card", secondary="activity_progress_locked_cards_rel",
                                   back_populates="activity_locked_cards")
    # cards_locked keeps track os the progresses' unlocked cards
    cards_unlocked = db.relationship("Card", secondary="activity_progress_unlocked_cards_rel",
                                     back_populates="activity_unlocked_cards")
    hints = db.relationship("HintStatus", cascade="all,delete", back_populates="activity")
    # checkpoints_incomplete keeps track of the incomplete checkpoints by the student
    checkpoints = db.relationship("CheckpointProgress", cascade="all,delete",
                                  back_populates="activity_checkpoints_progress")
    # checkpoints_failed keeps track of the checkpoint progresses where the student failed to fulfill the requirements
    checkpoints_failed = db.relationship("CheckpointProgress", secondary="activity_progress_checkpoint_failed_rel",
                                         back_populates="activity_failed")
    # checkpoints_passed keeps track of the checkpoint progresses where the student fulfilled the requirements
    checkpoints_passed = db.relationship("CheckpointProgress", secondary="activity_progress_checkpoint_passed_rel",
                                         back_populates="activity_passed")
    student = db.relationship("Student", back_populates="activity_progresses")
    activity = db.relationship("Activity", back_populates="students")


# Association object to keep track of the CheckpointProgress
class CheckpointProgress(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    activity_progress_id = db.Column(db.Integer, db.ForeignKey("activity_progress.id"))
    checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoint.id'))
    contentful_id = db.Column(db.Text, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    image_to_receive = db.Column(db.Text, nullable=True)
    video_to_receive = db.Column(db.Text, nullable=True)
    test_cases_failed = db.Column(db.Integer, nullable=True)
    test_cases_passed = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    checkpoint = db.relationship("Checkpoint", back_populates="activity_progresses")
    activity_checkpoints_progress = db.relationship("ActivityProgress", back_populates="checkpoints")
    # activity_passed keeps track of a failed checkpoint progress
    activity_failed = db.relationship("ActivityProgress", secondary="activity_progress_checkpoint_failed_rel",
                                      back_populates="checkpoints_failed")
    # activity_passed keeps track of a passed checkpoint progress
    activity_passed = db.relationship("ActivityProgress", secondary="activity_progress_checkpoint_passed_rel",
                                      back_populates="checkpoints_passed")


# Association object for Hint and Activity Progress. Keeps track of which hint is locked
class HintStatus(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    activity_progress_id = db.Column(db.Integer, db.ForeignKey("activity_progress.id"))
    hint_id = db.Column(db.Integer, db.ForeignKey('hint.id'))
    is_unlocked = db.Column(db.Boolean, nullable=False, default=False)

    # hint children and parent_hint_id allows a one to many relationship on itself
    parent_hint_id = db.Column(db.Integer, db.ForeignKey("hint_status.id"), nullable=True)
    hint_children = db.relationship("HintStatus", cascade="all,delete",
                                    backref=db.backref('parent_hint', remote_side='HintStatus.id'))
    hint = db.relationship("Hint", back_populates="activity_progresses")
    activity = db.relationship("ActivityProgress", back_populates="hints")


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

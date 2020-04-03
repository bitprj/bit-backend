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

# This many to many relationship keeps track of the activity progress' passed checkpoints
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
# This many to many relationship is used to keep track of which modules belong to a classroom and vice versa
classroom_modules_rel = db.Table("classroom_modules_rel",
                                 db.Column("classroom_id", db.Integer, db.ForeignKey("classroom.id")),
                                 db.Column("module_id", db.Integer, db.ForeignKey("module.id"))
                                 )

# This many to many relationship is used to keep track of which activities belong to module progress and vice versa
module_progress_completed_activities_rel = db.Table("module_progress_completed_activities_rel",
                                                    db.Column("module_progress_id", db.Integer,
                                                              db.ForeignKey("module_progress.id")),
                                                    db.Column("activity_id", db.Integer, db.ForeignKey("activity.id"))
                                                    )

# This many to many relationship is used to keep track of which activities belong to module progress and vice versa
module_progress_incomplete_activities_rel = db.Table("module_progress_incomplete_activities_rel",
                                                     db.Column("module_progress_id", db.Integer,
                                                               db.ForeignKey("module_progress.id")),
                                                     db.Column("activity_id", db.Integer, db.ForeignKey("activity.id"))
                                                     )

# This many to many relationship is used to keep track of which activities belong to module progress and vice versa
module_progress_inprogress_activities_rel = db.Table("module_progress_inprogress_activities_rel",
                                                     db.Column("module_progress_id", db.Integer,
                                                               db.ForeignKey("module_progress.id")),
                                                     db.Column("activity_id", db.Integer, db.ForeignKey("activity.id"))
                                                     )

# This many to many relationship is used to keep track of all of the topics that a student has completed
student_topic_completed_rel = db.Table("student_topic_completed_rel",
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

# This many to many relationship is used to keep track of all of the modules that a student has inprogress
student_module_inprogress_rel = db.Table("student_module_inprogress_rel",
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

# This many to many relationship is used to keep track of which modules belong to topic progress and vice versa
topic_progress_completed_modules_rel = db.Table("topic_progress_completed_modules_rel",
                                                db.Column("topic_progress_id", db.Integer,
                                                          db.ForeignKey("topic_progress.id")),
                                                db.Column("module_id", db.Integer, db.ForeignKey("module.id"))
                                                )

# This many to many relationship is used to keep track of which modules belong to topic progress and vice versa
topic_progress_incomplete_modules_rel = db.Table("topic_progress_incomplete_modules_rel",
                                                 db.Column("topic_progress_id", db.Integer,
                                                           db.ForeignKey("topic_progress.id")),
                                                 db.Column("module_id", db.Integer, db.ForeignKey("module.id"))
                                                 )

# This many to many relationship is used to keep track of which modules belong to topic progress and vice versa
topic_progress_inprogress_modules_rel = db.Table("topic_progress_inprogress_modules_rel",
                                                 db.Column("topic_progress_id", db.Integer,
                                                           db.ForeignKey("topic_progress.id")),
                                                 db.Column("module_id", db.Integer, db.ForeignKey("module.id"))
                                                 )

# This many to many relationship is used to keep track of which topics belong to track and vice versa
track_topic_rel = db.Table("track_topic_rel",
                           db.Column("track_id", db.Integer, db.ForeignKey("track.id")),
                           db.Column("topic_id", db.Integer, db.ForeignKey("topic.id"))
                           )

# This many to many relationship is used to keep track of which users belong to an event and vice versa
user_event_rel = db.Table("user_event_rel",
                          db.Column("user", db.Integer, db.ForeignKey("user.id")),
                          db.Column("event", db.Integer, db.ForeignKey("event.id"))
                          )

# This many to many relationship is used to keep track of which users are presenters in an event
user_presenter_event_rel = db.Table("user_presenter_event_rel",
                                    db.Column("user", db.Integer, db.ForeignKey("user.id")),
                                    db.Column("event", db.Integer, db.ForeignKey("event.id"))
                                    )

# This many to many relationship is used to keep track of which organizations belong to which user and vice versa
user_organization_rel = db.Table("user_organization_rel",
                                 db.Column("user", db.Integer, db.ForeignKey("user.id")),
                                 db.Column("organization", db.Integer, db.ForeignKey("organization.id"))
                                 )

# This many to many relationship is used to keep track of which users are a active in an organization
user_organization_active_rel = db.Table("user_organization_active_rel",
                                        db.Column("user", db.Integer, db.ForeignKey("user.id")),
                                        db.Column("organization", db.Integer, db.ForeignKey("organization.id"))
                                        )

# This many to many relationship is used to keep track of which users are a inactive in an organization
user_organization_inactive_rel = db.Table("user_organization_inactive_rel",
                                          db.Column("user", db.Integer, db.ForeignKey("user.id")),
                                          db.Column("organization", db.Integer, db.ForeignKey("organization.id"))
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
    github_id = db.Column(db.Integer, nullable=True)
    content_url = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)
    filename = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    summary = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.String(20), nullable=True)
    is_project = db.Column(db.Boolean, nullable=True)
    image = db.Column(db.Text, nullable=True)
    # cards keeps track of all the cards that is owned by an Activity
    cards = db.relationship("Card", cascade="all,delete", lazy="joined", back_populates="activity")
    # modules keeps track of all of the modules that an activity belongs to
    modules = db.relationship("Module", secondary="activity_module_rel", lazy="joined", back_populates="activities")
    # badge_prereqs keeps track of all the badge xp that are required to an activity
    badge_prereqs = db.relationship("ActivityBadgePrereqs", cascade="all,delete", lazy="joined",
                                    back_populates="activity")
    # modules keeps track of all of the modules that an activity belongs to
    module_prereqs = db.relationship("Module", secondary="activity_module_prereqs", lazy="joined",
                                     back_populates="activity_prereqs")
    # students_completed keeps track of which students have completed an activity
    students_completed = db.relationship("Student", secondary="student_activity_completed_rel",
                                         lazy="joined", back_populates="completed_activities")
    # students_incomplete keeps track of the students who have not completed an activity
    students_incomplete = db.relationship("Student", secondary="student_activity_incomplete_rel",
                                          lazy="joined", back_populates="incomplete_activities")
    # students_current keeps track of the activities that a student is working on
    students_current = db.relationship("Student", secondary="student_activity_current_rel",
                                       lazy="joined", back_populates="current_activities")
    # modules_completed keeps track of the activities completed in a module
    modules_completed = db.relationship("ModuleProgress", secondary="module_progress_completed_activities_rel",
                                        back_populates="completed_activities")
    # modules_incomplete keeps track of the activities that have not been completed in a module
    modules_incomplete = db.relationship("ModuleProgress", secondary="module_progress_incomplete_activities_rel",
                                         back_populates="incomplete_activities")
    # modules_inprogress keeps track of the activities are currently being worked on
    modules_inprogress = db.relationship("ModuleProgress", secondary="module_progress_completed_activities_rel",
                                         back_populates="inprogress_activities")
    # topic_prereqs keeps track of the activities that needs to be completed before accessing a topic
    topic_prereqs = db.relationship("Topic", secondary="topic_activity_prereqs", lazy="joined",
                                    back_populates="activity_prereqs")
    # last_module is the module in which the module unlocked last
    last_module = db.relationship("ModuleProgress", back_populates="last_activity_unlocked",
                                  foreign_keys="ModuleProgress.last_activity_unlocked_id")
    # chosen_module is the module in which the chosen_project is associated with
    chosen_module = db.relationship("ModuleProgress", back_populates="chosen_project",
                                    foreign_keys="ModuleProgress.chosen_project_id")
    # students keep track of the student's activity progress
    students = db.relationship("ActivityProgress", lazy="joined", back_populates="activity")
    # This is used to keep track of the student's actions for an activity
    actions = db.relationship("UserActivity", cascade="all,delete", back_populates="activity")
    parent_activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), nullable=True)
    prerequisite_activities = db.relationship("Activity",
                                              backref=db.backref('parent_activity', remote_side='Activity.id'))
    suggested_students = db.relationship("Student", back_populates="suggested_activity")

    def __init__(self, github_id, filename, name, description, summary, difficulty, image):
        self.github_id = github_id
        self.filename = filename
        self.name = name
        self.description = description
        self.summary = summary
        self.difficulty = difficulty
        self.image = image

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
    students = db.relationship("StudentBadges", cascade="all,delete", back_populates="badge")
    module_badge_weights = db.relationship("ModuleBadgeWeights", back_populates="badge")

    def __init__(self, contentful_id):
        self.contentful_id = contentful_id

    def __repr__(self):
        return f"Badge('{self.name}')"


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_url = db.Column(db.Text, nullable=True)
    github_raw_data = db.Column(db.Text, nullable=True)
    filename = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)
    gems = db.Column(db.Integer, nullable=True)
    # order is a number to keep track of the order in which this card will be displayed
    order = db.Column(db.Integer, nullable=True)
    # activity_id and activity keeps track of which lab the card is owned by
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"))
    activity = db.relationship("Activity", lazy="joined", back_populates="cards")
    checkpoint_id = db.Column(db.Integer, db.ForeignKey("checkpoint.id"))
    checkpoint = db.relationship("Checkpoint", cascade="all,delete", lazy="joined", back_populates="cards")
    # concepts keeps track of which concepts that the card owns
    concepts = db.relationship("Concept", secondary="card_concept_rel", lazy="joined", back_populates="cards")
    # hints keep track of the hints that a card owns
    hints = db.relationship("Hint", cascade="all,delete", lazy="joined", back_populates="card")
    # activity_locked_cards keep track of all the activities locked cards
    activity_locked_cards = db.relationship("ActivityProgress", lazy="joined",
                                            secondary="activity_progress_locked_cards_rel",
                                            back_populates="cards_locked")
    # activity_locked_cards keep track of all the activities unlocked cards
    activity_unlocked_cards = db.relationship("ActivityProgress", lazy="joined",
                                              secondary="activity_progress_unlocked_cards_rel",
                                              back_populates="cards_unlocked")

    def __init__(self, github_raw_data, name, gems, order, filename, activity_id):
        self.github_raw_data = github_raw_data
        self.name = name
        self.gems = gems
        self.order = order
        self.filename = filename
        self.activity_id = activity_id

    def __repr__(self):
        return f"Card('{self.name}')"


class Checkpoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_url = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)
    instruction = db.Column(db.Text, nullable=True)
    checkpoint_type = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text, nullable=True)
    cli_command = db.Column(db.Text, nullable=True)
    filename = db.Column(db.Text, nullable=True)
    test_cases_location = db.Column(db.Text, nullable=True)
    tests_zip = db.Column(db.Text, nullable=True)
    cards = db.relationship("Card", back_populates="checkpoint")
    criteria = db.relationship("Criteria", cascade="all,delete", back_populates="checkpoint")
    checkpoint_progresses = db.relationship("CheckpointProgress", back_populates="checkpoint")
    # choices represent the choices if the checkpoint is a multiple choice checkpoint
    choices = db.relationship("MCChoice", cascade="all,delete", back_populates="checkpoint",
                              foreign_keys="MCChoice.checkpoint_id")
    correct_choice = db.relationship("MCChoice", uselist=False, cascade="all,delete",
                                     back_populates="correct_checkpoint", foreign_keys="MCChoice.correct_checkpoint_id")
    # This is used to keep track of the student's actions for a checkpoint
    actions = db.relationship("UserCheckpoint", cascade="all,delete", back_populates="checkpoint")

    def __init__(self, name, instruction, checkpoint_type, filename):
        self.name = name
        self.instruction = instruction
        self.checkpoint_type = checkpoint_type
        self.filename = filename

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
    students = db.relationship('Student', secondary=students_classes_rel, lazy="joined", back_populates='classes')
    # modules keep track of all the modules that a teacher wants their students to learn
    modules = db.relationship("Module", secondary=classroom_modules_rel, lazy="joined", back_populates="classrooms")

    def __init__(self, name, teacher_id, date_start, date_end):
        self.name = name
        self.teacher_id = teacher_id
        self.date_start = date_start
        self.date_end = date_end

    def __repr__(self):
        return f"Class('{self.name}')"


class Concept(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_url = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)
    filename = db.Column(db.Text, nullable=True)
    # cards keep track of which cards that a concept belongs to
    cards = db.relationship("Card", secondary="card_concept_rel", lazy="joined", back_populates="concepts")
    # steps keep track of which steps that a concept owns
    steps = db.relationship("Step", cascade="all,delete", lazy="joined", back_populates="concept")

    def __init__(self, name, filename):
        self.name = name
        self.filename = filename

    def __repr__(self):
        return f"Concept('{self.name}')"


class Criteria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    criteria_key = db.Column(db.Text, nullable=True)
    checkpoint_id = db.Column(db.Integer, db.ForeignKey("checkpoint.id"), nullable=True)
    checkpoint = db.relationship("Checkpoint", back_populates="criteria")

    def __init__(self, content, criteria_key, checkpoint_id):
        self.content = content
        self.criteria_key = criteria_key
        self.checkpoint_id = checkpoint_id


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey("organization.id"), nullable=False)
    organization = db.relationship("Organization", back_populates="events")
    # presenters keep track of the users that are presenting at an event
    presenters = db.relationship("User", secondary="user_presenter_event_rel", back_populates="presenter_events")
    # rsvp_list keeps track of the users that are going to an event
    rsvp_list = db.relationship("User", secondary="user_event_rel", back_populates="rsvp_events")

    def __init__(self, name, date, summary, location, organization_id):
        self.name = name
        self.date = date
        self.summary = summary
        self.location = location
        self.organization_id = organization_id

    def __repr__(self):
        return f"Event('{self.name}')"


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
    content_url = db.Column(db.Text, nullable=True)
    github_raw_data = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)
    filename = db.Column(db.Text, nullable=True)
    gems = db.Column(db.Integer, nullable=True)
    order = db.Column(db.Integer, nullable=True)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"))
    card = db.relationship("Card", back_populates="hints")
    parent_hint_id = db.Column(db.Integer, db.ForeignKey("hint.id"), nullable=True)
    hints = db.relationship("Hint", cascade="all,delete",
                            backref=db.backref('parent_hint', remote_side='Hint.id'))
    # steps keep track of which steps a hint owns
    steps = db.relationship("Step", cascade="all,delete", back_populates="hint")
    activity_progresses = db.relationship("HintStatus", back_populates="hint")

    def __init__(self, name, gems, order, filename, github_raw_data):
        self.name = name
        self.gems = gems
        self.order = order
        self.filename = filename
        self.github_raw_data = github_raw_data

    def __repr__(self):
        return f"Hint('{self.name}')"


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_url = db.Column(db.Text, nullable=True)
    github_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.Text, nullable=True)
    filename = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    gems_needed = db.Column(db.Integer, nullable=True)
    image = db.Column(db.Text, nullable=True)
    # activities keeps track of all of the activities that belongs to a module
    activities = db.relationship("Activity", secondary="activity_module_rel", back_populates="modules")
    # topics keep track of all of the topics that a module belongs to
    topics = db.relationship("Topic", secondary="topic_module_rel", back_populates="modules")
    # activity_prereqs keeps track of all of the activities that are prereqs to a module
    activity_prereqs = db.relationship("Activity", secondary="activity_module_prereqs", back_populates="module_prereqs")
    # badges is used to keep track of the badge xp perquisite to access the Module
    badge_prereqs = db.relationship("ModuleBadgePrereqs", cascade="all,delete", back_populates="module")
    # badge_weights is used to keep track of the badge xp weights
    badge_weights = db.relationship("ModuleBadgeWeights", cascade="all,delete", back_populates="module")
    # topic_prereqs is used to keep track of modules that need to be completed before accessing a topic
    topic_prereqs = db.relationship("Topic", secondary="topic_module_prereqs", back_populates="module_prereqs")
    # students_completed keeps track of which students have completed a module
    students_completed = db.relationship("Student", secondary="student_module_completed_rel",
                                         back_populates="completed_modules")
    # students_inprogress keeps track of which students have inprogress a module
    students_inprogress = db.relationship("Student", secondary="student_module_inprogress_rel",
                                          back_populates="inprogress_modules")
    # students_incomplete keeps track of the students who have not completed a module
    students_incomplete = db.relationship("Student", secondary="student_module_incomplete_rel",
                                          back_populates="incomplete_modules")
    students = db.relationship("ModuleProgress", cascade="all,delete", back_populates="module")
    # classrooms keep track of all the modules that are associated with a classroom
    classrooms = db.relationship("Classroom", secondary=classroom_modules_rel, back_populates="modules")
    # completed_topics keeps track of all modules completed
    completed_topics = db.relationship("TopicProgress", secondary="topic_progress_completed_modules_rel",
                                       back_populates="completed_modules")
    # incomplete_topics keeps track of all the modules have not been started
    incomplete_topics = db.relationship("TopicProgress", secondary="topic_progress_incomplete_modules_rel",
                                        back_populates="incomplete_modules")
    # inprogress_topics keeps track of all the modules that are currently being worked on
    inprogress_topics = db.relationship("TopicProgress", secondary="topic_progress_inprogress_modules_rel",
                                        back_populates="inprogress_modules")

    # def __init__(self, filename, name, description, gems_needed, image):
    #     self.filename = filename
    #     self.name = name
    #     self.description = description
    #     self.gems_needed = gems_needed
    #     self.image = image

    def __repr__(self):
        return f"Module('{self.name}')"


class MCChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    choice_key = db.Column(db.Text, nullable=True)
    # checkpoint_id is to reference a MCChoice as a choice for a Multiple Choice Checkpoint
    checkpoint_id = db.Column(db.Integer, db.ForeignKey("checkpoint.id"))
    checkpoint = db.relationship("Checkpoint", back_populates="choices", foreign_keys=[checkpoint_id])
    # correct_checkpoint_id is to reference a MCChoice as the correct choice for a Multiple Choice Checkpoint
    correct_checkpoint_id = db.Column(db.Integer, db.ForeignKey("checkpoint.id"))
    correct_checkpoint = db.relationship("Checkpoint", back_populates="correct_choice",
                                         foreign_keys=[correct_checkpoint_id])

    def __init__(self, content, choice_key):
        self.content = content
        self.choice_key = choice_key

    def __repr__(self):
        return f"MCChoice('{self.id}')"


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    background_image = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    owners = db.relationship("User", secondary="user_organization_rel", back_populates="organizations")
    # active_users are used to keep track of which users are active in an organization
    active_users = db.relationship("User", secondary="user_organization_active_rel",
                                   back_populates="organizations_active")
    # inactive_users are used to keep track of which users are not active in an organization
    inactive_users = db.relationship("User", secondary="user_organization_inactive_rel",
                                     back_populates="organizations_inactive")
    events = db.relationship("Event", cascade="all,delete", back_populates="organization")

    def __init__(self, name, image, background_image, is_active):
        self.name = name
        self.image = image
        self.background_image = background_image
        self.is_active = is_active

    def __repr__(self):
        return f"Organization('{self.name}')"


class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_url = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)
    code_snippet = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text, nullable=True)
    # step_key is used to uniquely identify the step in the database
    step_key = db.Column(db.Text, nullable=True)
    # concept keeps track of concept that a step belongs to
    concept_id = db.Column(db.Integer, db.ForeignKey("concept.id"))
    concept = db.relationship("Concept", back_populates="steps")
    # hint keeps track of a hint that a step belongs to
    hint_id = db.Column(db.Integer, db.ForeignKey("hint.id"))
    hint = db.relationship("Hint", back_populates="steps")

    def __init__(self, name, step_key):
        self.name = name
        self.step_key = step_key

    def __repr__(self):
        return f"Step('{self.name}')"


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    results = db.Column(db.JSON, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    progress_id = db.Column(db.Integer, db.ForeignKey("checkpoint_progress.id"), nullable=False)
    progress = db.relationship("CheckpointProgress", back_populates="submissions")

    def __init__(self, results, progress_id, date_time):
        self.results = results
        self.progress_id = progress_id
        self.date_time = date_time

    def __repr__(self):
        return f"Submission('{self.id}')"


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_url = db.Column(db.Text, nullable=True)
    github_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.Text, nullable=True)
    filename = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text, nullable=True)
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
    # students_inprogress keeps track of the students that are currently on a topic
    students_inprogress = db.relationship("Student", secondary="student_topic_inprogress_rel",
                                          back_populates="inprogress_topics")
    students = db.relationship("TopicProgress", cascade="all,delete", back_populates="topic")

    # def __init__(self, github_id, name, description, image):
    #     self.github_id = github_id
    #     self.name = name
    #     self.description = description
    #     self.image = image

    def __repr__(self):
        return f"Topic('{self.name}')"


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_url = db.Column(db.Text, nullable=True)
    github_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.Text, unique=True, nullable=True)
    description = db.Column(db.Text, nullable=True)
    # topics keep track of which topics belong to a track
    topics = db.relationship("Topic", secondary="track_topic_rel", back_populates="tracks")
    # required topics keep track of the required topics that need to be completed by the user
    required_topics = db.relationship("Topic", secondary="track_topic_reqs", back_populates="required_tracks")
    # students keep track of which student is associated with a particular track
    students = db.relationship("Student", back_populates="current_track")

    # def __init__(self, github_id, name, description):
    #     self.github_id = github_id
    #     self.name = name
    #     self.description = description

    def __repr__(self):
        return f"Track('{self.name}')"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    # username is the email
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, unique=True, nullable=False)
    token = db.Column(db.Text, unique=True, nullable=True)
    # Roles are Admin, Teacher, or Student
    roles = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    location = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=True)
    organizations = db.relationship("Organization", secondary="user_organization_rel", back_populates="owners")
    organizations_active = db.relationship("Organization", secondary="user_organization_active_rel",
                                           back_populates="active_users")
    organizations_inactive = db.relationship("Organization", secondary="user_organization_inactive_rel",
                                             back_populates="inactive_users")
    # presenter_events keep track of the events that a user is presenting at
    presenter_events = db.relationship("Event", secondary="user_presenter_event_rel", back_populates="presenters")
    # rsvp_events keeps track of the events that the user has rsvp to
    rsvp_events = db.relationship("Event", secondary="user_event_rel", back_populates="rsvp_list")

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
    global_gems = db.Column(db.Integer, nullable=False, default=0)
    last_seen = db.Column(db.DateTime, nullable=True)
    # completed_activities keeps track of all activities that a student has completed
    completed_activities = db.relationship("Activity", secondary="student_activity_completed_rel",
                                           back_populates="students_completed")
    # incomplete_activities keeps track of all the activities that a student has not completed
    incomplete_activities = db.relationship("Activity", secondary="student_activity_incomplete_rel",
                                            back_populates="students_incomplete")
    # current_activities keeps track of all the activities that a student is working on
    current_activities = db.relationship("Activity", secondary="student_activity_current_rel",
                                         lazy="joined", back_populates="students_current")
    # completed_modules keeps track of all modules that a student has completed
    completed_modules = db.relationship("Module", secondary="student_module_completed_rel",
                                        back_populates="students_completed")
    # incomplete_topics keeps track of all the modules that a student has not completed
    incomplete_modules = db.relationship("Module", secondary="student_module_incomplete_rel",
                                         back_populates="students_incomplete")
    # inprogress_modules keeps track of all modules that a student has inprogress
    inprogress_modules = db.relationship("Module", secondary="student_module_inprogress_rel",
                                         back_populates="students_inprogress")
    # completed_topics keeps track of all the topics that a student has completed
    completed_topics = db.relationship("Topic", secondary="student_topic_completed_rel",
                                       back_populates="students_completed")
    # inprogress_topics keeps track of all the topics that a student has not completed
    inprogress_topics = db.relationship("Topic", secondary="student_topic_inprogress_rel",
                                        back_populates="students_inprogress")
    # current_track is used to keep track of the student's current track
    current_track_id = db.Column(db.Integer, db.ForeignKey("track.id"))
    current_track = db.relationship("Track", back_populates="students")
    # activity_progresses keeps track of all the progresses that a student has made on their activities
    activity_progresses = db.relationship("ActivityProgress", cascade="all,delete", back_populates="student")
    module_progresses = db.relationship("ModuleProgress", cascade="all,delete", back_populates="student")
    topic_progresses = db.relationship("TopicProgress", cascade="all,delete", back_populates="student")
    # classes keeps track of all the student's classes
    classes = db.relationship("Classroom", secondary=students_classes_rel, back_populates="students")
    badges = db.relationship("StudentBadges", cascade="all,delete", back_populates="student")
    actions = db.relationship("UserAction", cascade="all,delete", back_populates="student")
    suggested_activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), nullable=True)
    suggested_activity = db.relationship("Activity", back_populates="suggested_students")

    def __repr__(self):
        return f"Student('{self.id}')"


class Teacher(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    classrooms = db.relationship('Classroom', back_populates='teacher')

    def __repr__(self):
        return f"Teacher('{self.id}')"


class UserAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False)
    action = db.Column(db.Text, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    student = db.relationship("Student", back_populates="actions")

    def __init__(self, date_time, action):
        self.date_time = date_time
        self.action = action

    def __repr__(self):
        return f"StudentActivity('{self.action}')"


class UserActivity(UserAction):
    id = db.Column(db.Integer, db.ForeignKey("user_action.id"), primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"))
    activity = db.relationship("Activity", lazy="joined", back_populates="actions")

    def __repr__(self):
        return f"UserAction('{self.action}')"


class UserCheckpoint(UserAction):
    id = db.Column(db.Integer, db.ForeignKey("user_action.id"), primary_key=True)
    checkpoint_id = db.Column(db.Integer, db.ForeignKey("checkpoint.id"))
    checkpoint = db.relationship("Checkpoint", lazy="joined", back_populates="actions")

    def __repr__(self):
        return f"UserCheckpoint('{self.action}')"


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
    last_card_unlocked = db.Column(db.Integer, nullable=True)
    date_graded = db.Column(db.Date, nullable=True)
    accumulated_gems = db.Column(db.Integer, nullable=False)
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
    student_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=True)
    multiple_choice_is_correct = db.Column(db.Boolean, nullable=True, default=False)
    student_comment = db.Column(db.Text, nullable=True)
    teacher_comment = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    checkpoint = db.relationship("Checkpoint", lazy="joined", back_populates="checkpoint_progresses")
    activity_checkpoints_progress = db.relationship("ActivityProgress", back_populates="checkpoints")
    submissions = db.relationship("Submission", cascade="all,delete", back_populates="progress")
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
    card_id = db.Column(db.Integer, nullable=True)
    is_unlocked = db.Column(db.Boolean, nullable=False, default=False)

    # hint children and parent_hint_id allows a one to many relationship on itself
    parent_hint_id = db.Column(db.Integer, db.ForeignKey("hint_status.id"), nullable=True)
    hints = db.relationship("HintStatus", cascade="all,delete",
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


# Association object for modules and badges. This is for prerequisites
class ModuleBadgeWeights(db.Model):
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), primary_key=True)
    weight = db.Column(db.Float, nullable=False)

    module = db.relationship("Module", back_populates="badge_weights")
    badge = db.relationship("Badge", back_populates="module_badge_weights")


# Association object for modules and students. Used to keep track of the gems that user has accumulated for each module
class ModuleProgress(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    gems = db.Column(db.Integer, nullable=False)

    # last_activity is the last activity unlocked in a module
    last_activity_unlocked_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    last_activity_unlocked = db.relationship("Activity", back_populates="last_module",
                                             foreign_keys=[last_activity_unlocked_id])
    # chosen_project is the project chosen for a module
    chosen_project_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    chosen_project = db.relationship("Activity", back_populates="chosen_module",
                                     foreign_keys=[chosen_project_id])

    # completed_activities keeps track of all activities completed
    completed_activities = db.relationship("Activity", secondary="module_progress_completed_activities_rel",
                                           back_populates="modules_completed")
    # incomplete_activities keeps track of all the activities have not been started
    incomplete_activities = db.relationship("Activity", secondary="module_progress_incomplete_activities_rel",
                                            back_populates="modules_incomplete")
    # inprogress_activities keeps track of all the activities that are currently being worked on
    inprogress_activities = db.relationship("Activity", secondary="module_progress_inprogress_activities_rel",
                                            back_populates="modules_inprogress")
    module = db.relationship("Module", back_populates="students")
    student = db.relationship("Student", back_populates="module_progresses")


# Association object to keep track of the student's badge progress
class StudentBadges(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), primary_key=True)
    # This contentful_id refers to the contentful id of the badge
    contentful_id = db.Column(db.Text, nullable=False)
    xp = db.Column(db.Integer, nullable=False)

    student = db.relationship("Student", back_populates="badges")
    badge = db.relationship("Badge", back_populates="students")


# Association object for topics and badges. This is for prerequisites
class TopicBadgePrereqs(db.Model):
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey("badge.id"), primary_key=True)
    xp = db.Column(db.Integer, nullable=False)

    badge = db.relationship("Badge", back_populates="topics")
    topic = db.relationship("Topic", back_populates="badge_prereqs")


# Association object for topics and students. Used to keep track of the incomplete, inprogress, and completed activities
class TopicProgress(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    is_completed = db.Column(db.Boolean, nullable=False, default=False)

    # completed_modules keeps track of all modules completed
    completed_modules = db.relationship("Module", secondary="topic_progress_completed_modules_rel",
                                        back_populates="completed_topics")
    # incomplete_modules keeps track of all the modules have not been started
    incomplete_modules = db.relationship("Module", secondary="topic_progress_incomplete_modules_rel",
                                         back_populates="incomplete_topics")
    # inprogress_modules keeps track of all the modules that are currently being worked on
    inprogress_modules = db.relationship("Module", secondary="topic_progress_inprogress_modules_rel",
                                         back_populates="inprogress_topics")
    topic = db.relationship("Topic", back_populates="students")
    student = db.relationship("Student", back_populates="topic_progresses")

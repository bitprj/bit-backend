from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_praetorian import Praetorian
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from backend.config import *
from contentful_management import Client

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_ACCESS_LIFESPAN'] = {'minutes': 45}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 1}
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_POOL_SIZE'] = 60000
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)
guard = Praetorian()
ma = Marshmallow()
migrate = Migrate(app, db)
contentful_client = Client(CONTENT_MANGEMENT_API_KEY)


from backend.models import User

guard.init_app(app, User)

from backend.activities.routes import activities_bp
from backend.activity_progresses.routes import activity_progresses_bp
from backend.authentication.routes import authentication_bp
from backend.badges.routes import badges_bp
from backend.cards.routes import cards_bp
from backend.checkpoints.routes import checkpoints_bp
from backend.checkpoint_progresses.routes import checkpoint_progresses_bp
from backend.classrooms.routes import classrooms_bp
from backend.concepts.routes import concepts_bp
from backend.gems.routes import gems_bp
from backend.hints.routes import hints_bp
from backend.modules.routes import modules_bp
from backend.steps.routes import steps_bp
from backend.students.routes import students_bp
from backend.topics.routes import topics_bp
from backend.tracks.routes import tracks_bp

app.register_blueprint(activities_bp)
app.register_blueprint(activity_progresses_bp)
app.register_blueprint(authentication_bp)
app.register_blueprint(badges_bp)
app.register_blueprint(cards_bp)
app.register_blueprint(checkpoints_bp)
app.register_blueprint(checkpoint_progresses_bp)
app.register_blueprint(classrooms_bp)
app.register_blueprint(concepts_bp)
app.register_blueprint(gems_bp)
app.register_blueprint(hints_bp)
app.register_blueprint(modules_bp)
app.register_blueprint(steps_bp)
app.register_blueprint(students_bp)
app.register_blueprint(topics_bp)
app.register_blueprint(tracks_bp)

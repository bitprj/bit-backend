from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_praetorian import Praetorian
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from backend.config import *
from contentful_management import Client
from github import Github
from itsdangerous import URLSafeTimedSerializer
import pusher

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY
# app.config["JWT_ACCESS_LIFESPAN"] = {"minutes": 45}
# app.config["JWT_REFRESH_LIFESPAN"] = {"days": 1}
# Change token expires later to some time
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
app.config["MAIL_SERVER"] = MAIL_SERVER
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD
app.config["MAIL_PORT"] = MAIL_PORT
app.config["MAIL_USE_TLS"] = MAIL_USE_TLS
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_SIZE"] = 70000
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_SECRET_KEY"] = SECRET_KEY
app.config["CORS_HEADERS"] = "Content-Type"
app.config["PROPAGATE_EXCEPTIONS"] = True

api = Api(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
guard = Praetorian()
mail = Mail(app)
safe_url = URLSafeTimedSerializer(SECRET_KEY)
ma = Marshmallow()
migrate = Migrate(app, db)
# CORS(app,  supports_credentials=True, resources={r"/*": {"origins": ["http://localhost:3000"]}})
CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["*"]}})
git = Github(GITHUB_ACCESS_TOKEN)
repo = git.get_repo(GITHUB_REPO)
contentful_client = Client(CONTENT_MANGEMENT_API_KEY)
pusher_client = pusher.Pusher(
    app_id=PUSHER_APP_ID,
    key=PUSHER_KEY,
    secret=PUSHER_SECRET,
    cluster=PUSHER_CLUSTER,
    ssl=True)

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
from backend.criteria.routes import criteria_bp
from backend.events.routes import events_bp
from backend.gems.routes import gems_bp
from backend.hints.routes import hints_bp
from backend.hooks.routes import hooks_bp
from backend.mc_choices.routes import mc_choices_bp
from backend.modules.routes import modules_bp
from backend.organizations.routes import organizations_bp
from backend.module_progresses.routes import module_progresses_bp
from backend.steps.routes import steps_bp
from backend.students.routes import students_bp
from backend.teachers.routes import teachers_bp
from backend.topics.routes import topics_bp
from backend.topic_progresses.routes import topic_progresses_bp
from backend.tracks.routes import tracks_bp
from backend.track_progresses.routes import track_progresses_bp

app.register_blueprint(activities_bp)
app.register_blueprint(activity_progresses_bp)
app.register_blueprint(authentication_bp)
app.register_blueprint(badges_bp)
app.register_blueprint(cards_bp)
app.register_blueprint(checkpoints_bp)
app.register_blueprint(checkpoint_progresses_bp)
app.register_blueprint(classrooms_bp)
app.register_blueprint(concepts_bp)
app.register_blueprint(criteria_bp)
app.register_blueprint(events_bp)
app.register_blueprint(gems_bp)
app.register_blueprint(hints_bp)
app.register_blueprint(hooks_bp)
app.register_blueprint(mc_choices_bp)
app.register_blueprint(modules_bp)
app.register_blueprint(module_progresses_bp)
app.register_blueprint(organizations_bp)
app.register_blueprint(steps_bp)
app.register_blueprint(students_bp)
app.register_blueprint(teachers_bp)
app.register_blueprint(topics_bp)
app.register_blueprint(topic_progresses_bp)
app.register_blueprint(tracks_bp)
app.register_blueprint(track_progresses_bp)

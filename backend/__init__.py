from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_praetorian import Praetorian
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from backend.config import *

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_ACCESS_LIFESPAN'] = {'minutes': 10}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 1}
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_POOL_SIZE'] = 60000
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)
guard = Praetorian()
ma = Marshmallow()
migrate = Migrate(app, db)

from backend.models import User
guard.init_app(app, User)


from backend.authentication.routes import authentication_bp
from backend.badges.routes import badges_bp
from backend.gems.routes import gems_bp
from backend.modules.routes import modules_bp
from backend.topics.routes import topics_bp
from backend.tracks.routes import tracks_bp

app.register_blueprint(authentication_bp)
app.register_blueprint(badges_bp)
app.register_blueprint(gems_bp)
app.register_blueprint(modules_bp)
app.register_blueprint(topics_bp)
app.register_blueprint(tracks_bp)

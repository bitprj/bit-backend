from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from backend.config import *

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_POOL_SIZE'] = 60000
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow()
migrate = Migrate(app, db)
db.init_app(app)

from backend.badges.routes import badges_bp
from backend.gems.routes import gems_bp
from backend.activities.routes import activities_bp

app.register_blueprint(badges_bp)
app.register_blueprint(gems_bp)
app.register_blueprint(activities_bp)

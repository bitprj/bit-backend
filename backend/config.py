import os
from dotenv import load_dotenv
from os.path import dirname, join

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

S3_BUCKET = os.environ.get('S3_BUCKET')
S3_BUCKET = os.environ.get('S3_CDN_BUCKET')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_LOCATION = os.environ.get('AWS_LOCATION')

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = os.environ.get('SECRET_KEY')
ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')


PUSHER_APP_ID = os.environ.get('PUSHER_APP_ID')
PUSHER_KEY = os.environ.get('PUSHER_KEY')
PUSHER_SECRET = os.environ.get('PUSHER_SECRET')
PUSHER_CLUSTER = os.environ.get('PUSHER_CLUSTER')

INSTANCE_LOCATOR = os.environ.get('INSTANCE_LOCATOR')
CHAT_API = os.environ.get('CHAT_API')

MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')

CONTENT_MANGEMENT_API_KEY = os.environ.get("CONTENT_MANGEMENT_API_KEY")
CONTENT_DELIVERY_API_KEY = os.environ.get("CONTENT_DELIVERY_API_KEY")
SPACE_ID = os.environ.get("SPACE_ID")

GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")
API = os.environ.get("API")

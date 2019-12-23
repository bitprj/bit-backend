from backend.config import S3_BUCKET
from flask_praetorian.utilities import current_guard
import boto3
import urllib.parse
import urllib.request


# Function to upload an image to s3 based on the folder
def add_image(file, folder):
    s3_client = boto3.client('s3')
    path = 'darlene/' + folder + '/' + file.filename
    s3_client.put_object(Bucket=S3_BUCKET, Key=path, Body=file)
    url = 'https://projectbit.s3-us-west-1.amazonaws.com/darlene/' + folder + '/' + file.filename
    image = urllib.parse.quote(url, "\./_-:")
    return image


# Function to retrieve the user id from a  jwt token
def get_user_id_from_token():
    guard = current_guard()
    token = guard.read_token_from_header()
    jwt_data = guard.extract_jwt_token(token)

    return jwt_data["id"]

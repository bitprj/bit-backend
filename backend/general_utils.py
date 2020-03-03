from backend import repo
from backend.config import S3_BUCKET
from PIL import Image
from urllib.request import urlopen
import boto3
import io
import re
import urllib.parse
import urllib.request


# Function to upload an image to s3 based on the folder
def add_file(image_bytes, folder, filename):
    s3_client = boto3.client('s3')
    path = 'Github/' + folder + '/' + filename
    s3_client.put_object(Bucket=S3_BUCKET, Key=path, Body=image_bytes)
    url = 'https://projectbit.s3-us-west-1.amazonaws.com/Github/' + folder + '/' + filename
    image = urllib.parse.quote(url, "\./_-:")

    return image


# Function to create an image object
def create_image_obj(data):
    # Gets the image path
    regex = r'\(([^)]+)'
    image_name = re.search(regex, data["image"]).group(1)
    image_path = data["image_folder"] + image_name
    # Get the download image url from github
    image_url = repo.get_contents(path=image_path).download_url
    image = Image.open(urlopen(image_url))
    # Save the image as bytes to send to S3
    image_bytes = io.BytesIO()
    image.save(image_bytes, format=image.format)
    image_bytes.seek(0)

    return add_file(image_bytes, "modules", image_name[7:])

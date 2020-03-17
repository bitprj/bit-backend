from backend import repo
from backend.config import S3_BUCKET
from bs4 import BeautifulSoup as BS
from PIL import Image
from urllib.request import urlopen
from zipfile import ZipFile
import boto3
import io
import os
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


def create_image_obj(image_name, image_path, folder):
    # Get the download image url from github
    image_url = repo.get_contents(path=image_path).download_url
    image = Image.open(urlopen(image_url))
    # Save the image as bytes to send to S3
    image_bytes = io.BytesIO()
    image.save(image_bytes, format=image.format)
    image_bytes.seek(0)

    return add_file(image_bytes, folder, image_name[7:])


# Function to parse files from github and save them locally
def create_zip(test_file_location):
    os.chdir("./github")
    files = repo.get_contents(test_file_location)
    zip_file = ZipFile('tests.zip', 'w')
    files_to_send = write_files(files)

    for file in files_to_send:
        zip_file.write(file)

    zip_file.close()

    return files_to_send


# Function to delete all the files created
def delete_files(files):
    for file in files:
        os.remove(file)

    os.remove("tests.zip")
    os.chdir("..")

    return


# Function to parse an image tag for its name
def parse_img_tag(image, image_folder, folder):
    # Gets the image path
    soup = BS(image, features="html.parser")
    image_name = None

    for image in soup.find_all('img'):
        image_name = image["src"]
    image_path = image_folder + image_name

    if "https" in image_path:
        return image_name
    else:
        return create_image_obj(image_name, image_path, folder)


# Function to submit a tests.zip file
def send_tests_zip(filename):
    s3_resource = boto3.resource('s3')
    path = 'Github/test_cases/' + filename + "/tests.zip"
    s3_resource.meta.client.upload_file('tests.zip', S3_BUCKET, path)
    zip_link = 'https://projectbit.s3-us-west-1.amazonaws.com/' + path

    return zip_link


# Function to write to the files from github
def write_files(files):
    files_to_send = []

    for file in files:
        filename = file.path.split("/")[-1]
        content = file.decoded_content.decode("utf-8")
        f = open(filename, 'w')
        f.write(content)
        files_to_send.append(filename)
        f.close()

    return files_to_send

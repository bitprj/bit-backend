from backend import repo
from backend.activities.schemas import activity_schema
from backend.cards.schemas import card_schema
from backend.checkpoints.schemas import checkpoint_schema
from backend.concepts.schemas import concept_schema
from backend.config import S3_BUCKET, S3_CDN_BUCKET
from backend.hints.schemas import hint_schema
from backend.modules.schemas import module_schema
from backend.topics.schemas import topic_schema
from backend.tracks.schemas import track_schema
from bs4 import BeautifulSoup as BS
from PIL import Image
from urllib.request import urlopen
from zipfile import ZipFile
import boto3
import io
import json
import os
import requests
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


# Binary search function to search by object id
def binary_search(array, l, r, target):
    while l <= r:
        mid = l + (r - l) // 2
        if array[mid].id == target:
            return mid
        elif array[mid].id < target:
            l = mid + 1
        else:
            r = mid - 1
    return -1


# Function to remove white space in dictionary keys
def clear_white_space(readme_data):
    new_data = {}

    for name, data in readme_data.items():
        # Gets rid of white space in the dictionary key
        no_space_name = name.strip().lower()

        if isinstance(data, dict):
            # Recurse if the value is a dictionary
            data = clear_white_space(data)

        if isinstance(data, str):
            # Gets rid of white space in the dictionary value
            new_data[no_space_name] = data.strip()
        else:
            new_data[no_space_name] = data

    return new_data


def create_image_obj(image_name, image_path, folder):
    # Get the download image url from github
    image_url = repo.get_contents(path=image_path).download_url
    image = Image.open(urlopen(image_url))
    # Save the image as bytes to send to S3
    image_bytes = io.BytesIO()
    image.save(image_bytes, format=image.format)
    image_bytes.seek(0)

    return add_file(image_bytes, folder, image_name[7:])


# Function to create a json file based on the schema type and send it to s3
def create_schema_json(model_obj, schema_type):
    schema = get_schema(schema_type)
    schema_data = schema.dump(model_obj)
    data_filename = model_obj.filename.split("/")
    data_path = "/".join(data_filename[:-1])
    filename = model_obj.name.replace(" ", "_") + "_" + str(model_obj.id) + ".json"
    url = send_file_to_cdn(schema_data, data_path, filename)

    return url


# Function to parse files from github and save them locally
def create_zip(test_file_location):
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


# Function to choose a schema to return data
def get_schema(schema_type):
    if schema_type == "track":
        return track_schema
    elif schema_type == "topic":
        return topic_schema
    elif schema_type == "module":
        return module_schema
    elif schema_type == "activity":
        return activity_schema
    elif schema_type == "concept":
        return concept_schema
    elif schema_type == "card":
        return card_schema
    elif schema_type == "hint":
        return hint_schema
    elif schema_type == "checkpoint":
        return checkpoint_schema


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
    path = 'Github/test_cases/' + filename + "/tests.zip"
    with open('tests.zip', 'rb') as data:
        s3 = boto3.client('s3')
        s3.upload_fileobj(data, S3_BUCKET, path)
    zip_link = 'https://projectbit.s3-us-west-1.amazonaws.com/' + path

    return zip_link


# Function to store file data into a file and send them to s3
# This is used for md and json files
def send_file_to_cdn(data, file_path, filename):
    # if "cdn" in os.getcwd():
    #     os.chdir("..")
    # os.chdir("./cdn")

    if isinstance(data, dict):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    elif isinstance(data, str):
        with open(filename, "w") as f:
            content = requests.get(data)
            f.write(content.text)

    s3_client = boto3.client("s3")
    path = file_path + "/" + filename
    s3_client.upload_file(filename, S3_CDN_BUCKET, path)
    url = "https://d36nt3c422j20i.cloudfront.net/" + path

    # if "cdn" in os.getcwd():
    os.remove(filename)

    return url


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

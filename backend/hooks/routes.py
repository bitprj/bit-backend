from flask import Blueprint, request
from flask_restful import Resource
from backend import api
from backend.config import API
from backend.hooks.parse_utils import parse_files, store_files
from backend.hooks.utils import edit_test_json, get_files
import requests

# Blueprint for hooks
hooks_bp = Blueprint("hooks", __name__)


# git add .
# git commit -m "Testing hooks"
# git push origin test

# git add .
# git commit -m "Testing hooks"
# git push


# Class to handle merge requests
class ReceiveMerge(Resource):
    def post(self):
        data = request.get_json()
        files = {}

        # if data["ref"] == "refs/heads/master":
        files = get_files(data["commits"])
        files_to_change = files[0]
        files_to_delete = files[1]

        for filename in files_to_delete.keys():
            if filename in files_to_change:
                files_to_change.pop(filename)

        print(files_to_delete)
        print(files_to_change)

        stored_files = store_files(files_to_change)
        module_files = stored_files[0]
        activity_files = stored_files[1]
        concept_files = stored_files[2]
        card_files = stored_files[3]
        parse_files(module_files, activity_files, concept_files, card_files)

        for file in files_to_delete.values():
            if "Concept" in file:
                data["filename"] = file
                requests.delete(API + "/concepts", json=data)

            if "Module" in file and "Activity" not in file and "README.md" in file:
                data["filename"] = file
                requests.delete(API + "/modules", json=data)

            if "Module" in file and "Activity" in file and "README.md" in file:
                data["filename"] = file
                requests.delete(API + "/activities", json=data)

            if "Module" in file and "Activity" in file and "Cards" in file and file.endswith(".md"):
                card_name = file.split("/")[-1]
                card_name = card_name.split(".")[0]
                name_length = len(card_name) - 2

                if name_length < 0:
                    data = {"filename": file}
                    requests.delete(API + "/cards", json=data)
                else:
                    data = {"filename": file}
                    requests.delete(API + "/hints", json=data)

        # if "tests.json" in files_to_change:
        #     edit_test_json(files_to_change["tests.json"])

        return "ok", 200


api.add_resource(ReceiveMerge, "/merge")

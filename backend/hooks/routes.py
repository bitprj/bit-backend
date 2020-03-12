from flask import Blueprint, request
from flask_restful import Resource
from backend import api
from backend.config import API
from backend.hooks.utils import edit_test_json, get_files, md_to_json, parse_activity, parse_concept, parse_module
from backend.models import Card
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

        # for filename in files_to_delete.keys():
        #     file = files_to_change.pop(filename)
        #     files_removed.append(file)

        print(files_to_delete)
        print(files_to_change)

        for file in files_to_change.values():
            if "Concepts" in file.filename and "images" not in file.filename:
                parse_concept(file)

            if "Module" in file.filename and "Activity" in file.filename and "README.md" in file.filename:
                parse_activity(file)

            if "Module" in file.filename and "Activity" not in file.filename and "README.md" in file.filename:
                parse_module(file)

            # if "Module" in file.filename and "Activity" in file.filename and file.filename.endswith(
            #         ".md") and "README.md" not in file.filename:
            #     parse_card(file)

        for file in files_to_delete.values():
            if "Concept" in file:
                data["filename"] = file
                requests.delete(API + "/concepts", json=data)

            if "Module" in file and "Activity" not in file and "README.md" in file:
                data["filename"] = file
                requests.delete(API + "/modules", json=data)

            if "Module" in file and "Activity" in file and "README.md" in file:
                data["filename"] = file
                # data = md_to_json(files_to_delete[file.filename].raw_url)
                # data["github_id"] = int(data["github_id"])
                requests.delete(API + "/activities", json=data)

        #     if "Module" in file.filename and "Activity" in file.filename and file.filename.endswith(
        #             ".md") and "README.md" not in file.filename:
        #         card_name = file.filename.split("/")[2]
        #         card_name = card_name.split(".")[0]
        #         name_length = len(card_name) - 2
        #
        #         if name_length < 0:
        #             data = {"filename": file.filename}
        #             requests.delete(API + "/cards", json=data)
        #         else:
        #             data = {"filename": file.filename}
        #             requests.delete(API + "/hints", json=data)

        # if "tests.json" in files_to_change:
        #     edit_test_json(files_to_change["tests.json"])

        return "ok", 200


api.add_resource(ReceiveMerge, "/merge")

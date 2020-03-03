from flask import Blueprint, request
from flask_restful import Resource
from backend import api
from backend.config import API
from backend.hooks.utils import edit_test_json, get_files, md_to_json, parse_module
import requests

# Blueprint for hooks
hooks_bp = Blueprint("hooks", __name__)
# git add .
# git commit -m "Testing hooks"
# git push origin test


# Class to handle merge requests
class ReceiveMerge(Resource):
    def post(self):
        data = request.get_json()
        files = {}

        if data["ref"] == "refs/heads/master":
            files = get_files(data["commits"])
            files_to_change = files[0]
            files_removed = files[1]
            files_to_delete = {}

            for filename in files_to_change.keys():
                if filename in files_removed:
                    files_to_delete[filename] = files_to_change[filename]

            for filename in files_to_delete.keys():
                files_to_change.pop(filename)

            print(files_to_delete)
            print(files_to_change)

            for file in files_to_change.values():
                if "Module" in file.filename and "README.md" in file.filename:
                    parse_module(file)

            for file in files_to_delete.values():
                if "Module" in file.filename and "README.md" in file.filename:
                    data = md_to_json(files_to_delete[file.filename].raw_url)
                    data["github_id"] = int(data["github_id"])
                    requests.delete(API + "/modules", json=data)

            if "tests.json" in files_to_change:
                edit_test_json(files)

        return "ok", 200


api.add_resource(ReceiveMerge, "/merge")

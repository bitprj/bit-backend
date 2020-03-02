from flask import Blueprint, request
from flask_restful import Resource
from backend import api
from backend.hooks.utils import edit_test_json, get_files, parse_module

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
            print(files)
            if "tests.json" in files:
                edit_test_json(files)
                files.pop("tests.json")

            for file in files.values():
                if "Module" in file.filename and "README.md" in file.filename:
                    parse_module(file)
                    # do stuff
                    print(":')")

        return "ok", 200


api.add_resource(ReceiveMerge, "/merge")

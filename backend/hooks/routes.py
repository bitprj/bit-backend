from flask import Blueprint, request
from flask_restful import Resource
from backend import api
from backend.hooks.delete_utils import delete_files
from backend.hooks.parse_utils import parse_files, store_files
from backend.hooks.utils import edit_test_json, get_files

# Blueprint for hooks
hooks_bp = Blueprint("hooks", __name__)


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
        topic_files = stored_files[0]
        module_files = stored_files[1]
        activity_files = stored_files[2]
        concept_files = stored_files[3]
        card_files = stored_files[4]
        checkpoint_files = stored_files[5]
        test_case_files = stored_files[6]
        parse_files(topic_files, module_files, activity_files, concept_files, card_files, checkpoint_files,
                    test_case_files)
        delete_files(files_to_delete)

        # if "tracks.json" in files_to_change:
        #     edit_test_json(files_to_change["tracks.json"])

        return "ok", 200


api.add_resource(ReceiveMerge, "/merge")

# MCQuestion

Created: Jan 24, 2020 9:20 PM

**MCQuestion Model**

description - the question

contentful_id - id from contentful

checkpoint_id - references the checkpoint that the multiple choice question model belongs to

choices - references the choices to choose from a MC question

correct_choice - references the correct choice of the MC question

**MCQuestion in Contentful**

description - the question

choices - references the choices to choose from a MC question

correct_choice - references the correct choice of the MC question

**GET** FetchMCQuestion - `api.bitproject.org/mc_questions/{{mc_question_id}}`

This call is used to fetch an mc_question from the database. It returns, the name, contentful_id,  choices and correct_choice.

    {
        "id": 1,
        "contentful_id": "73pJdf5Qbo4N3l4KfHfKq",
        "choices": [
            {
                "id": 4,
                "contentful_id": "7uXvL38wFUUuPsBYgV8Tlj"
            },
            {
                "id": 8,
                "contentful_id": "6stbK9KUbxUf0ww80sm95n"
            }
        ],
        "correct_choice": {
            "id": 4,
            "contentful_id": "7uXvL38wFUUuPsBYgV8Tlj"
        }
    }

**POST** CreateMCQuestion - `api.bitproject.org/mc_questions`

This call is used to create a new mc_question. It takes a webhook from contentful to receive the contentful id.

    {"entityId": "73pJdf5Qbo4N3l4KfHfKq"}

**PUT**  UpdateMCQuestion - `api.bitproject.org/mc_questions`

This call is used to update an existing mc_question. It receives the choices, correct_choice and description from a webhook and updates it in the database.

    {
      "entityId": "73pJdf5Qbo4N3l4KfHfKq",
      "contentType": {
        "sys": {
          "type": "Link",
          "linkType": "ContentType",
          "id": "multipleChoiceQuestion"
        }
      },
      "spaceId": "aq4puo31m564",
      "parameters": {
        "description": {
          "en-US": "How to print hello world in python?"
        },
        "mc_choices": {
          "en-US": [
            {
              "sys": {
                "type": "Link",
                "linkType": "Entry",
                "id": "7uXvL38wFUUuPsBYgV8Tlj"
              }
            },
            {
              "sys": {
                "type": "Link",
                "linkType": "Entry",
                "id": "6stbK9KUbxUf0ww80sm95n"
              }
            }
          ]
        },
        "correct_choice": {
          "en-US": {
            "sys": {
              "type": "Link",
              "linkType": "Entry",
              "id": "7uXvL38wFUUuPsBYgV8Tlj"
            }
          }
        }
      }
    }

**We use a POST request to delete data from contentful!**

**POST** DeleteMCQuestion - `api.bitproject.org/mc_questions`

This call is used to delete an existing mc_question. It receives a contentful id from a webhook and deletes it in the backend.

    {"entityId": "73pJdf5Qbo4N3l4KfHfKq"}
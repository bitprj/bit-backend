# MCChoice

Created: Jan 24, 2020 9:36 PM

**MCChoice Model**

content - the content of the choice

contentful_id - id from contentful

mc_question_id - a reference to keep track of which MCQuestion that a MCChoice belongs to

**MCChoice in Contentful**

content - the content of the choice

**GET** FetchMCChoice - `api.bitproject.org/mc_choices/{{mc_choice_id}}`

This call is used to fetch a mc_choice from the database. It returns, the name, contentful_id,  choices and correct_choice.

    {
        "id": 4,
        "contentful_id": "6stbK9KUbxUf0ww80sm95n"
    }

**POST** CreateMCChoice - `api.bitproject.org/mc_choices`

This call is used to create a new mc_choice. It takes a webhook from contentful to receive the contentful id.

    {"entityId": "6stbK9KUbxUf0ww80sm95n"}

**PUT**  UpdateMCChoice - `api.bitproject.org/mc_choices`

This call is used to update an existing mc_choices. It receives the choices, correct_choice and description from a webhook and updates it in the database.

    {
      "entityId": "6stbK9KUbxUf0ww80sm95n",
      "contentType": {
        "sys": {
          "type": "Link",
          "linkType": "ContentType",
          "id": "choice"
        }
      },
      "spaceId": "aq4puo31m564",
      "parameters": {
        "content": {
          "en-US": "print('Hello World')"
        }
      }
    }

**We use a POST request to delete data from contentful!**

**POST** DeleteMCChoice - `api.bitproject.org/mc_choices`

This call is used to delete an existing mc_choices. It receives a contentful id from a webhook and deletes it in the backend.

    {"entityId": "6stbK9KUbxUf0ww80sm95n"}
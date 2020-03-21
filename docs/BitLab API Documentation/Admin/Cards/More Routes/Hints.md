# Hints

Created: Dec 15, 2019 12:50 AM

**Hint Model**

name - name of the hint

contentful_id - id from contentful

**Hint in Contentful**

name - name of concept

difficulty - difficulty of the hint

gems - gems that the student spends when opening a hint

steps - the steps of a concept

**GET** FetchHint- `api.bitproject.org/hints/{{hint_id}}`

This call is used to retrieve a hint from the database. It returns the id, contentful_id, name, difficulty, gems, cards' contentful ids and steps contentful ids.

    {
        "id": 13,
        "contentful_id": "15OczOY0R9REOEY227faLh",
        "name": "Hint 1",
        "parent": null,
        "steps": [
            {
                "id": 57,
                "contentful_id": "rTHzVrvt5arAS2PEaLn4B",
                "heading": "delete step 1"
            },
            {
                "id": 58,
                "contentful_id": "2KdmuFR8toG4yAmIK7ROgt",
                "heading": "delete 2 step"
            }
        ]
    }

**POST** CreateHint- `api.bitproject.org/hints`

This call is used to create a new hint. Sends the entry id through a webhook from contentful and saves it to the database.

    {"entityId": "4hlj5866GRIUxvEGyO89Zk"}

**PUT**  UpdateHint- `api.bitproject.org/hints`

This call is used to update an existing hint. Updates the name of the card when updated in contentful.

    {
      "entityId": "15OczOY0R9REOEY227faLh",
      "spaceId": "aq4puo31m564",
      "parameters": {
        "name": {
          "en-US": "Hint 1"
        },
        "steps": {
          "en-US": [
            {
              "sys": {
                "type": "Link",
                "linkType": "Entry",
                "id": "rTHzVrvt5arAS2PEaLn4B"
              }
            },
            {
              "sys": {
                "type": "Link",
                "linkType": "Entry",
                "id": "2KdmuFR8toG4yAmIK7ROgt"
              }
            }
          ]
        }
      }
    }

**We use a POST request to delete data from contentful!**

**POST** DeleteHint - `api.bitproject.org/hints/delete`

This call is used to delete an existing card. Sends the entry id through a webhook from contentful and deletes it in the database.

    {"entityId": "4hlj5866GRIUxvEGyO89Zk"}
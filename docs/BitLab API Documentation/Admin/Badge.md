# Badge

Created: Jan 02, 2020 10:07 PM

**Badge Model**

name - name of the badge

contentful_id - id from contentful

**Badge in Contentful**

name - name of badge

description - a brief description about the badge

threshold - shows what level the badge would level up with exp

image - image of the badge

**GET** FetchBadge- `api.bitproject.org/badges/{{badge_id}}`

This call is used to retrieve a card from the database. It returns the id, contentful_id, hint contentful_ids and concept contentful_ids.

    {
        "id": 9,
        "contentful_id": "j93EqZmEWHIFRhTTzLMEQ",
        "name": "Intro to Programming"
    }

**POST** CreateBadge- `api.bitproject.org/badges`

This call is used to create a new badge. Sends the entry id through a webhook from contentful and saves it to the database.

    {
      "entityId": "j93EqZmEWHIFRhTTzLMEQ"
    }

**PUT**  UpdateBadge- `api.bitproject.org/badges`

This call is used to update an existing card. Updates the name of the card when updated in contentful.

    {
      "entityId": "j93EqZmEWHIFRhTTzLMEQ",
      "spaceId": "aq4puo31m564",
      "parameters": {
        "name": {
          "en-US": "Intro to Programming"
        }
      }
    }

**We use a POST request to delete data from contentful!**

**POST** DeleteBadge - `api.bitproject.org/badges/delete`

This call is used to delete an existing card. Sends the entry id through a webhook from contentful and deletes it in the database.

    {
      "entityId": "j93EqZmEWHIFRhTTzLMEQ"
    }
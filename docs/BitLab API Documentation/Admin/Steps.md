# Steps

Created: Jan 02, 2020 2:34 AM

**Step Model**

heading - name of the step

contentful_id - id from contentful

**Step in Contentful**

heading - name of step

content - content in step

order - order of step

image - image of the Step

**GET** FetchStep- `api.bitproject.org/steps/{{step_id}}`

This call is used to retrieve a step from the database. It returns the id, contentful_id, and heading.

    {
        "id": 49,
        "contentful_id": "5wibkpWgziZ7HGc7stNfqR",
        "heading": "Downloading VSCode"
    }

**POST** CreateStep- `api.bitproject.org/steps`

This call is used to create a new step. Sends the entry id through a webhook from contentful and saves it to the database.

    {"entityId": "5wibkpWgziZ7HGc7stNfqR"}

**PUT**  UpdateStep- `api.bitproject.org/steps`

This call is used to update an existing step. Updates the name of the card when updated in contentful.

    {
      "entityId": "5wibkpWgziZ7HGc7stNfqR",
      "spaceId": "aq4puo31m564",
      "parameters": {
        "heading": {
          "en-US": "Downloading VSCode "
        }
      }
    }

**We use a POST request to delete data from contentful!**

**POST** DeleteStep - `api.bitproject.org/steps/delete`

This call is used to delete an existing card. Sends the entry id through a webhook from contentful and deletes it in the database.

    {"entityId": "5wibkpWgziZ7HGc7stNfqR"}
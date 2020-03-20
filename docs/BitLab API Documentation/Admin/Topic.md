# Topic

Created: Dec 15, 2019 12:31 AM

![Modules/Screen_Shot_2019-12-11_at_1.18.29_PM.png](Modules/Screen_Shot_2019-12-11_at_1.18.29_PM.png)

**Topic Model**

github_id - The id that uniquely identifies a topic in the tracks.json file on Github. The id is a number

name - Name of the topic

description - Something that describes what the topic aims to teach a person

modules - The modules that are associated with a topic

**GET** FetchTopic - `api.bitproject.org/topics/{{topic_id}}`

This call is used to fetch a topic from the database. It returns the following JSON data.

    {
        "id": 6,
        "github_id": 2,
        "name": "World",
        "description": "Default description and other things stuff",
        "modules": [1]
    }

**POST** CreateTopic - `api.bitproject.org/topics`

This call is used to create a new topic. 

To create a Topic, add it to a Track's topics in the tracks.json file. It must have the following parameters:

- github_id - The id that uniquely identifies a topic in the tracks.json file
- name - name of the object
- description - a description about the topic
- modules - list of module github_ids

**Note: If the above parameters are not in the object, then the Topic will not be created in the database.**

    {
        "github_id": 2,
        "name": "World",
        "description": "Default description and other things stuff",
        "modules": [1]
    }

**PUT**  UpdateTopic- `api.bitproject.org/topics`

This call is used to update an existing topic. 

To update a Topic, update it in a Track's topics in the tracks.json file. It must have the following parameters:

- github_id - The id that uniquely identifies a topic in the tracks.json file
- name - name of the object
- description - a description about the topic
- modules - list of module github_ids

**Note: If the above parameters are not in the object, then the Topic will not be updated in the database.**

    {
        "github_id": 2,
        "name": "The World",
        "description": "Default description and other things stuff",
        "modules": [1]
    }

**DELETE** DeleteTopic - `api.bitproject.org/topics`

This call is used to delete an existing topic tin Github. It expects to receive the github_id to delete the object in the database.

**Note: This call will only be called if the topic is not associated in any Tracks in the database.**

    {
    	"github_id": 1
    }
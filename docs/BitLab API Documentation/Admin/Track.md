# Track

Created: Dec 14, 2019 11:47 PM

![Track/Screen_Shot_2019-12-11_at_12.59.32_PM.png](Track/Screen_Shot_2019-12-11_at_12.59.32_PM.png)

**Track Model**

github_id - The id that uniquely identifies a track in the tracks.json file on Github. The id is a number

name - Name of the track

description - Something that describes what the track aims to teach a person

topics - The topics that are associated with a track

students - The students who are currently in a track

**GET** FetchTrack - `api.bitproject.org/tracks/{{track_id}}`

This call is used to fetch a track from the database. It returns the following JSON data.

    {
        "id": 16,
        "github_id": 1,
        "name": "Computer Science",
        "description": "Some description about computer science and other things",
        "topics": [
            {
                "id": 1,
                "github_id": 1,
                "name": "Hello "
            },
            {
                "id": 6,
                "github_id": 2,
                "name": "World"
            }
        ]
    }

**GET** FetchTracks - `api.bitproject.org/tracks/all`

This call is used to fetch all the tracks in the database. It returns the following JSON data.

    [
        {
            "id": 1,
            "github_id": 3,
            "name": "Track 1",
            "description": "Default description and other things",
            "topics": [
                {
                    "id": 8,
                    "github_id": 4,
                    "name": "Things"
                }
            ]
        },
        {
            "id": 15,
            "github_id": 2,
            "name": "Chemistry",
            "description": "Some description about chemistry and other things stuff",
            "topics": [
                {
                    "id": 7,
                    "github_id": 3,
                    "name": "More"
                },
                {
                    "id": 2,
                    "github_id": 5,
                    "name": "Topic 1"
                },
                {
                    "id": 1,
                    "github_id": 1,
                    "name": "Hello "
                }
            ]
        }
    ]

**POST** CreateTrack - `api.bitproject.org/tracks`

This call is used to create a new track. This call expects the following JSON data to be received to create a new Track. 

Set the Track to a JSON object. The name of the Track would be the key and set it to an object with the following parameters: 

- a github_id
- a name
- a description
- an array of topic objects

Topic object parameters:

- github_id - The id that uniquely identifies a topic in the tracks.json file
- name - name of the object
- description - a description about the topic
- modules - list of module github_ids

**Note: If the above parameters are not in the object, then the Track will not be created in the database.**

    "Computer Science": {
            "github_id": 1,
            "name": "Computer Science",
            "description": "Some description about computer science and other things",
            "topics": [
                {
                    "github_id": 1,
                    "name": "Hello ",
                    "description": "Default description and other things stuff"
                },
                {
                    "github_id": 2,
                    "name": "World",
                    "description": "Default description and other things stuff"
                }
            ]
        }

**PUT**  UpdateTrack - `api.bitproject.org/tracks`

This call is used to update an existing track. This call expects the following JSON data to be received.

Set the Track to a JSON object. The name of the Track would be the key and set it to an object with the following parameters: 

- a github_id which is manually inputted
- a name
- a description
- an array of topic objects

Topic object parameters:

- github_id - The id that uniquely identifies a topic in the tracks.json file
- name - name of the object
- description - a description about the topic
- modules - list of module github_ids

**Note: If the above parameters are not in the object, then the Track will not be updated in the database.**

    "Computer Science Engineering": {
            "github_id": 1,
            "name": "Computer Science Engineering",
            "description": "Some description about computer science and other things",
            "topics": [
                {
                    "github_id": 1,
                    "name": "Hello ",
                    "description": "Default description and other things stuff"
                },
                {
                    "github_id": 2,
                    "name": "World",
                    "description": "Default description and other things stuff"
                }
            ]
        }

**Delete** DeleteTrack - `api.bitproject.org/tracks`

This call is used to delete an existing track through the tracks.json file on Github. It expects to receive the github_id to delete the object in the database.

    {
    	"github_id": 1
    }
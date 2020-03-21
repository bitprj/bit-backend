# Track

Created: Dec 14, 2019 7:33 PM

**GET** FetchTrack - `api.bitproject.org/track/{track_id}/fetch`

Initialize Track View with title, focus, description, modules associated

    {
    	"id": 12345,
    	"track": "Computer Science",
    	"focus": "Full Stack",
    	"description": "Description Lorem Ipsum",
    	"image": "some image url",
    	"required_topics": [{
    								"order": 1,
    								"id": 12345,
    								"topic_title": "Programming Principles",
    								"modules": [{
    								"id": 12345,
    								"module_title": "Programming Principles",
    								},...
    							]
    					},...
    					]
    	"saved_topics": [{
    								"order": 4,
    								"id": 12351545,
    								"topic_title": "Programming Dancing",
    								"modules": [{
    								"id": 123435255,
    								"module_title": "Programming Dancing Intro",
    								},...
    							]
    					},...
    					]
    }
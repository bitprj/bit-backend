# Track Progress

Created: Dec 15, 2019 1:35 AM

completed_topics - many to many with student

incompleted_topics - many to many with student

inprogress_topics - many to many with s

**GET** FetchTrackProgress - `api.bitproject.org/tracks/{{track_id}}/progress`

Return the progress on completion on a particular track 
( return all topics that have been completed within the provided track id)

    {
    	"completed_topics": [
    							{
    								"id": 1,
    								"title": "HTML/CSS/JS",
    								"Description": "Teaches the basics of web development."
    							}
    						],
    	"incomplete_topics": [ 
    								{
    									"id": 2,
    									"title": "MERN",
    									"Description": "Teaches the fullstack development with a MERN stack"T
    								}
    							]
    	"current_topic": {
    											"id": 3,
    											"title": "VUE",
    											"Description": "Teaches vue.js"
    										}
    }

**PUT** AddTopic - `api.bitproject.org/tracks/progress/<int:topic_id>/add_topic`

A route to add modules to a student's inprogress topic column.

**Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.**

    {
    	"message": "Topic added!"
    }

**UPDATE - Add topic if all modules have been completed**

**PUT** UpdateTrackProgress - `api.bitproject.org/tracks/progress/{{topic_id}}`

Updates the track progress by the topic id.

**Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.**

    {
        "message": "Student topic successfully updated!"
    }
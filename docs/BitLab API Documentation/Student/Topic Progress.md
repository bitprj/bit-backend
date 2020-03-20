# Topic Progress

Created: Dec 23, 2019 10:01 PM

**GET** FetchTopicProgress - `api.bitproject.org/topics/{{topic_id}}/progress`

Return the progress on completion on a particular topic 
( return all modules that have been completed within the provided topic id )

    {
    	"completed_modules": [
    												{
    													"id": 1,
    													"name": "Intro to Python",
    													"Description": "Teaches introductory Python"
    													"icon": "Some url"
    												}
    											],
    	"incomplete_modules": [ 
    													{
    														"id": 2,
    														"name": "Advance Python",
    														"Description": "Teaches Advance Python"
    														"icon": "Some url"
    													}
    												]
    }

**PUT** AddModule - `api.bitproject.org/topics/{{topic_id}}/progress/<int:module_id>/add`

A route to add modules to a student's inprogress column.

**Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.**

    {
    	"message": "Module added!"
    }

**PUT** UpdateTopicProgress - `api.bitproject.org/topics/{{topic_id}}/progress/<int:module_id>`

Adds a module to a student's module completed progress. If all of the modules are completed for a topic then the topic gets added to the student's completed topics.

**Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.**

    {
        "message": "Successfully updated student completed modules"
    }
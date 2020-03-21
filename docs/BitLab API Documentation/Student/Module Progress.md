# Module Progress

Created: Dec 21, 2019 11:34 PM

**GET** FetchModuleProgress - `api.bitproject.org/modules/{{module_id}}/progress`

Return the progress on completion on a particular module 
( return all lab that have been completed within the provided module id )

    {
    	"completed_activities": [
    														{
    															"id": 1,
    															"name": "Python if statments",
    															"Description": "Teaches Python if statements",
    															"icon": "Some url"
    														}
    													],
    	"incomplete_activities": [ 
    														{
    															"id": 2,
    															"name": "Python for loops",
    															"Description": "Teaches Advance Python",
    															"icon": "Some url"
    														}
    													]
    }

**PUT** UpdateModuleProgress - `api.bitproject.org/modules/{{module_id}}/progress/update`

Return the progress on completion on a particular topic 
( return a lab that have been completed within the provided module id )

**Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.**

    {
    	"complete": {
    							"id": 47
    						}
    }
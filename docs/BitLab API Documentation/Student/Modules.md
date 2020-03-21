# Modules

Created: Dec 14, 2019 6:52 PM

**GET** FetchModule - `api.bitproject.org/module/{module_id}/fetch`

Initialize Module View with title, description, url, and link to the particular activity. 

    {
    	id: 12345,
    	module_title: "Programming Principles",
    	activities: [{
    						id: 12345,
    						activity_title: "Activity Title", 
    						activity_description: "Activity Description",
    						activity_thumbnail: "Activity
    					},...
    					],
    	selected_projects: [14235, 23242] // id of all selected projects. if null show choose a project modal
    }

### **Choose Lab Modal**

**GET** FetchLabs - `api.bitproject.org/module/{module_id}/labs/all`

Load Modal to select lab

    {
    	"id": 12345,
    	"gem_threshold": 300,
    	"current_gem": 400,
    	"projects": [{
    						"id": 12345,
    						"project_title": "Project Title", 
    						"project_description": "Project Description",
    						"project_thumbnail": "Project Thumbnail link"
    						"gem": 400
    					},...
    					]
    }

**PUT** SelectLabs

`api.bitproject.org/module/{module_id}/labs/select`

Mark labs as "selected" when user chooses in modal

    {
    	id: 45040
    }
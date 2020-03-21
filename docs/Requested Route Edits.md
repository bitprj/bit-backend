# Requested Route Edits

additional notes:

- activities are reusable
    - everything underneath it (requiring progress) is not reusable (unique to the activity) like checkpoints, hints....
    - for example, if a new module has an activity that was already completed, then it'll show up as complete, etc
    - this may have some interesting implications for grading
- classrooms are not reusable

# FetchTeacherData

---

route: *GET*`/teachers/data`

- all classrooms teacher is in charge of

### Potential Response (change as necessary)

---

    "classrooms": [
    	{
    		"id": "1"
    	},
    	{
    		"id": "7"
    	}
    ]

# FetchClassroom

---

    "id": "1",
    "name": "Bryan's Python course",
    "date_start": "2020-01-04",
    "date_end": "2020-04-23",
    "class_code": "kPAdB",
    "teacher": {
    	"id": "12"
    },
    "students": [
    	{
    		"id": "13"
    	},
    	{
    		"id": "73"
    	}
    ],
    "modules": [
    	{
    		"id": "13",
        "activities": [
    			"id": "12",
    		]
    ]

# FetchSubmissions (already exists)

---

route (change to): *GET* `/classrooms/{{classroom_id}}/{{activity_id}}/grade` 

If there are no activities then return an empty array.

- submission id
- student data

### Potential Response (change as necessary)

# FetchSubmissionsAll

---

route: GET `/classrooms/{{classroom_id}}/grade`
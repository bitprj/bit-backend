# Classroom

Created: Dec 26, 2019 1:09 AM

Classroom model:

name - name of class

date_start - date started of classroom

date_end - date end of classroom

class_code - code to join this classroom

teacher_id

teacher - teacher that owns the class

students - students in the classroom

**GET** FetchClassroom - `api.bitproject.org/classrooms/{{classroom_id}}`

This call is used to fetch a classroom from the database. It returns, the name, date_start, date_end and class_code

    {
        "name": "Bryan's classroom",
        "date_start": "2020-01-04",
        "date_end": "2020-04-23",
        "class_code": "0sxU1",
        "teacher": {
            "name": "Teacher",
            "username": "Teacher@example.com"
        },
        "students": [
            {
                "name": "Student 3",
                "username": "Student3@example.com"
            }
        ]
    }

**POST** CreateClassroom- `api.bitproject.org/classrooms`

**Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.**

This call is used to create a new card. Sends the entry id through a webhook from contentful and saves it to the database.

    {
    	"name": "Bryan's classroom",
    	"date_start": "2020-1-4",
    	"date_end": "2020-4-23"
    }

**PUT**  UpdateActivity - `api.bitproject.org/classrooms/{{classroom_id}}`

**Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.**

This call is used to update an existing activity.

    {
    	"name": "Bryan's Python Class",
    	"date_start": "2020-1-4",
    	"date_end": "2020-4-23"
    }

**DEL** DeleteClassroom - `api.bitproject.org/classrooms/{{classroom_id}}`

**Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.**

This call is used to delete an existing classroom based on classroom id

    {
        "message": "Classroom successfully deleted"
    }
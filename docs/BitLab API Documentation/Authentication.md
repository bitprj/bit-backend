# Authentication

Authenticating and Validating Users on Bitlab

**POST** CreateAdmin- `api.bitproject.org/admins/create`

This call is used to create a new admin.

    {
    	"name": "Admin",
    	"username": "Admin@example.com",
    	"password": "donuts",
    	"roles": "Admin",
    	"image": "some_image_file",
    	"location": "Davis"
    }

**POST** CreateTeacher- `api.bitproject.org/teachers/create`

This call is used to create a new teacher.

    {
    	"name": "Teacher",
    	"username": "Teacher@example.com",
    	"password": "donuts",
    	"roles": "Teacher",
    	"image": "some_image_file",
    	"location": "Davis"
    }

**POST** CreateStudent- `api.bitproject.org/students/create`

This call is used to create a new student.

    {
    	"name": "Student",
    	"username": "Student@example.com",
    	"password": "donuts",
    	"roles": "Student",
    	"image": "some_image_file",
    	"location": "Davis"
    }

**PUT** Edit User - `api.bitproject.org/user/edit`

This call is used to edit a user.

    // data sent to the sever
    {
    	"name": "Setting up VS Code",
    	"username": "food@example.com",
    	"password": "donuts",
    	"image": "some_image_file", 
    	"location": "Vacaville"
    }

**POST** Login - `api.bitproject.org/auth`

This call is used to login a user

    {
    	"message": "You have been successfully logged in."
    }

**DEL** Logout - `api.bitproject.org/user/logout`

This call is used to logout a user

    {
    	"message": "You have been successfully logged out."
    }
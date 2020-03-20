# Using Marshmallow to Simplify Parameter Validation in APIs

Assigned: Bryan Wong, Daniel Kim
Status: Writing

![Using%20Marshmallow%20to%20Simplify%20Parameter%20Validation/Pitch_Deck.png](Using%20Marshmallow%20to%20Simplify%20Parameter%20Validation/Pitch_Deck.png)

Recently, I created a RESTful API with Flask where my models had many parameters. While working on it, I noticed that I was writing a lot of code to validate the data in each request. This led to long hours of debugging through the spaghetti code I wrote. I am now beginning a second project and want to avoid the same spaghetti validation from my first app. Thankfully, there is a package called *Marshmallow* to mediate this problem. 

# The Problem

To illustrate the problem I had, I'm going to write about one of our real endpoints for the Learning Management System (LMS) we are developing. 

One of the models in our database is the Activity model, which has the following parameters:

- name
- description
- summary
- difficulty
- image
- gem_amount
- criteria_1
- criteria_2
- criteria_3
- date_created
- cards
- concepts
- lab_prereqs
- module_prereqs
- topic_prereqs

That's a lot of parameters for one model. In Flask, without a validation library, your code might look something like this:

    # Function to validate form data for activities
    def validate(form_data):
        if "name" not in form_data:
            return {"message": "Missing form parameters."}, 500
    
        if type(form_data["name"]) != str:
            return {"message": "Wrong input type."}, 500
    
        if len(form_data["name"]) > 40:
            return {"message": "Parameter is too long."}, 500
    
        if "description" not in form_data:
            return {"message": "Missing form parameters."}, 500
    
        if type(form_data["description"]) != str:
            return {"message": "Wrong input type."}, 500
    
        if len(form_data["description"]) > 70:
            return {"message": "Parameter is too long."}, 500
    
        if "gem_amount" not in form_data:
            return {"message": "Missing form parameters."}, 500
    
        if type(form_data["gem_amount"]) != int:
            return {"message": "Wrong input type."}, 500
    
        if "module_prereqs" not in form_data:
            return {"message": "Missing form parameters."}, 500
    
        if type(form_data["module_prereqs"]) != list:
            return {"message": "Wrong input type."}, 500
    
    # more validation goes here :(
        
        lab = create_lab(form_data)
        
        return lab

I didn't include every parameter or else you'd be reading forever. At this point, you can see that this code is difficult to read and time-consuming to write. We can separate this out to functions and make it more modular, but that still means we have to write a lot of code just for one model. This makes it difficult to manage because if you want to add more parameters to your model, then you have to go back to the validation function and add two to three more "if" statements for data validation. Great, more spaghetti code...

Thankfully, there is a validation package called *Marshmallow* to save the day. *Marshmallow* is a package that helps with serializing and deserializing objects.

# What is Serialization?

Serialization is the process of transforming an object into a format that can be stored or transmitted. Typically in Flask apps, we use SQLAlchemy to handle our database management. However, there is one problem: front-end frameworks like React don't understand how to read SQLAlchemy objects. This is where *Marshmallow* comes into play. *Marshmallow* is used to transform our SQLAlchemy objects into readable JSON data. *Marshmallow* also helps with the reverse— it can transform JSON data back into its original object from the serialized format. 

# *Marshmallow* Schemas

*Marshmallow* keeps track of the format of data through Schemas. A Schema is used to dictate the format of data sent to the server. It defines the fields that are accepted and validates the data types of the fields. 

You can define *Marshmallow* Schemas as the following:

    from marshmallow import fields, Schema
    
    # This schema is used to validate the activity form data
    class ActivityFormSchema(Schema):
    # The below fields are what the schema expects to 
        name = fields.Str(required=True)
        description = fields.Str(required=True)
        image = fields.Str(required=True)
        badge_prereqs = fields.List(fields.Dict(), required=True)
        module_prereqs = fields.List(fields.Int(), required=True)
    
    # More fields go here...
        
    		class Meta:
            # Fields to show when sending data
            fields = ("name", "description", "image", "badge_prereqs", "module_prereqs")
    
    
    activity_form_schema = ActivityFormSchema()

In this example, the ActivityFormSchema class checks the existence of the fields that you defined as well as validating the data type of the field. As you can see, this is more efficient than writing a thousand "if" statements. Now, we can validate our models with just one simple, powerful class. 

Here is an example of what the ActivityFormSchema expects to receive: 

    {
    		"name": "For loops",
    		"description": "Introduces the concept of for loops in Python.",
    		"image": "Some image url",
    		"badge_prereqs": [
    												{
    														"id": 1,
    														"xp": 400
    												},
    												{
    														"id": 4,
    														"xp": 200
    												}
    											],
    		"moudle_prereqs": [1, 2, 3]
    
    }

Even though we've defined the class, we still need to add some logic to control when the validation.

# *Marshmallow* Schema Logic

We would define our logic in the following route:

    from backend.activities.schemas import activity_form_schema
    
    class ActivityCreate(Resource):
        # Function to create a activity
        def post(self):
    				# This receives the data from the frontend
            form_data = request.get_json()
    				# This below validates the JSON data existence and data type 
            errors = activity_form_schema.validate(form_data)
    
            if errors:
                return {
                           "message": "Missing or sending incorrect data to create an activity. Double check the JSON data that it has everything needed to create an activity."
                       }, 500
            else:
    						# if all the fields from the schema exist in the JSON data and
    						# they are all valid, then the create activity function is called
    						create_activity()
    
            return {"message": "Activity successfully created"}, 202
    
    api.add_resource(ActivityCreate, "/activities/create")

If you happen to send invalid JSON data, then you would receive the error message. An example of invalid data would be assigning the name field with an integer instead of a string, as shown below:

    {
    		"name": 11,
    		"description": "Introduces the concept of for loops in Python.",
    		"image": "Some image url",
    		"badge_prereqs": [
    												{
    														"id": 1,
    														"xp": 400
    												},
    												{
    														"id": 4,
    														"xp": 200
    												}
    											],
    		"moudle_prereqs": [1, 2, 3]
    }

# *Marshmallow* Validators

We're almost done now. The only thing we need to do now is to add more validators. *Marshmallow* comes with some built-in validators so that we can restrict our Schemas even further. Here is an example:

    from marshmallow import fields, Schema
    from marshmallow.validate import Length
    
    # This schema is used to validate the activity form data
    class ActivityFormSchema(Schema):
        name = fields.Str(required=True, valdiate=Length(max=100))
        description = fields.Str(required=True, valdiate=Length(max=100))
        image = fields.Str(required=True, valdiate=Length(max=1000))
        badge_prereqs = fields.List(fields.Dict(), required=True)
        module_prereqs = fields.List(fields.Int(), required=True)
    
    # More fields go here...
        
    		class Meta:
            # Fields to show when sending data
            fields = ("name", "description", "image", "badge_prereqs", "module_prereqs")
    
    
    activity_form_schema = ActivityFormSchema()

In the example above, we imported Length from *Marshmallow* and applied it to our string fields. Now, whenever we try to validate our JSON data, it will check if our string fields go over the maximum amount of characters allowed. This is very powerful since this allows users to have even more control over what data gets passed through. The best part is that validators barely add any extra code! To look at more validators that *Marshmallow* offers, click the following link to learn more: 

[API Reference - marshmallow 3.3.0 documentation](https://marshmallow.readthedocs.io/en/stable/api_reference.html#module-marshmallow.validate)

# Nesting Schemas

At this point, you might be wondering, "How do we represent one-to-many, and many-to-many relationships with *Marshmallow*?" Luckily, *Marshmallow* has a special field called Nested to help with these types of situations. 

Let's say we have a Student model, and we want to create a many-to-many relationship with our Activity model. We would first create our StudentSchema. It would look something like this:

    from marshmallow import fields, Schema
    
    class StudentSchema(Schema):
        name = fields.Str(required=True)
        username = fields.Email(required=True)
        roles = fields.Str(required=False)
        image = fields.Str(required=True)
    
        class Meta:
            # Fields to show when sending data
            fields = ("name", "username", "roles", "image")
            ordered = True
    
    student_schema = StudentSchema()

Next, to add the relationship for both Student and Activity Schemas, we would add the following fields below:

    # This goes in the StudentSchema fields
    activities = fields.Nested(“ActivitySchema”, only=("name", "description", "image"), many=True)

    # This goes in the ActivitySchema fields
    students = fields.Nested(“StudentSchema”, only=("name", "username", "roles", "image"), many=True)

### What we did:

- We defined a Nested field in each Schema.
- In the Nested field, we specified the schema that we want to relate to in double quotation marks. (Note: In StudentSchema, we put “ActivitySchema” in its Nested field because we want our StudentSchema to have many ActivitySchemas.)
- We used the many parameters in each Schema to show that we want to display many AcivitySchemas in the StudentSchema and vice versa.
- The only parameter specifies what fields we want from the other Schema. (For example, in the StudentSchema, we only want to retrieve the name, description, and image from the ActivitySchema.)

# Nested Fields Solve Circular Referencing

The reason why we use the only parameter in the Nested fields is to prevent circular referencing. 

For example, we would have a problem if we defined our Schemas to look like this:

    # StudentSchema
    activities = fields.Nested(“ActivitySchema”, many=True)

    # ActivitySchema
    students = fields.Nested("StudentSchema", many=True)

Upon first glance, this seems perfectly fine, but there is a major problem with this. If you do not use the only parameter, then the StudentSchema will reference all of the ActivitySchema's fields. This means that the StudentSchema will use the Students field from the ActivitySchema, which references itself. This leads to a circular import since the StudentSchema is trying to reference itself through the ActivitySchema. That's why you use the only parameter— it is used to specify which fields you want your Schema to reference. Typically, it is used to reference every field except Nested fields. 

# The Result

With *Marshmallow,* we can write simple and powerful code to validate the data being sent and received from our server without writing too many "if" statements. Instead, all we have to do is declare a class, add some logic, and *Marshmallow* will take care of the rest. In the end, we get the following Schemas:

    from marshmallow import fields, Schema
    from marshmallow.validate import Length
    
    # This schema is used to validate the activity form data
    class ActivityFormSchema(Schema):
        name = fields.Str(required=True, valdiate=Length(max=100))
        description = fields.Str(required=True, valdiate=Length(max=100))
        image = fields.Str(required=True, valdiate=Length(max=1000))
        badge_prereqs = fields.List(fields.Dict(), required=True)
        module_prereqs = fields.List(fields.Int(), required=True)
    		students = fields.Nested(“StudentSchema”, only=("name", "username", "roles", "image"), many=True)
    # More fields go here...
        
    		class Meta:
            # Fields to show when sending data
            fields = ("name", "description", "image", "badge_prereqs", "module_prereqs")
    
    
    activity_form_schema = ActivityFormSchema()

    from marshmallow import fields, Schema
    
    class StudentSchema(Schema):
        name = fields.Str(required=True)
        username = fields.Email(required=True)
        roles = fields.Str(required=False)
        image = fields.Str(required=True)
    		activities = fields.Nested(“ActivitySchema”, only=("name", "description", "image"), many=True)
        class Meta:
            # Fields to show when sending data
            fields = ("name", "username", "roles", "image")
            ordered = True
    
    student_schema = StudentSchema()

# The Main Takeaway

- *Marshmallow* makes it easy to serialize and deserialize objects in Flask.
- *Marshmallow* makes it easy to check for the existence and data types of fields.
- *Marshmallow* already has built-in validators to further restrict the format of data being received or sent.
- *Marshmallow* makes it easy to nest Schemas within other Schemas while avoiding circular referencing.
- *Marshmallow* reduces the amount of code to write (AKA no more spaghetti code)!
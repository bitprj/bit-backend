# Build gems Model

Date Created: Dec 13, 2019 2:48 PM
Deadline: Dec 15, 2019
Property: Bryan Wong
Status: Done 🙌

Model:

amount - int

type - string

student - model (One to one)

Create the Postman request for the below routes

POST Create Gems

    {
    	id: 123
    }

PUT Edit Gem Amount

    {
    	id: 123,
    	gem_adjustment: -10
    }

DELETE Destroy Gem Model

    {
    	id: 123,
    	message: "Gem was successfully deleted"
    }
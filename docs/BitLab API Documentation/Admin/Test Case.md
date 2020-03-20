# Test Case

Created: Dec 27, 2019 11:52 PM

Model:

- checkpoint_id
- checkpoint
- input
- output

**POST** CreateCheckpoint - `api.bitproject.org/activities/{{activity_id}}/checkpoints/create`

This call is used to create a new checkpoint

    // data sent to the sever
    {
    	"name": "Checkpoint for code",
    	"test_cases": "some test cases"
    }

**PUT** CreateCheckpoint - `api.bitproject.org/checkpoints/{{check_point}}`

This call is used to create a new checkpoint

    // data sent to the sever
    {
    	"name": "Checkpiont for code and stuff",
    	"test_cases": "some test cases"
    }

**DEL** DeleteCheckpoint - `api.bitproject.org/checkpoints/{{checkpoint_id}}`

This call is used to delete a checkpoint

    {
    	"message": "Checkpoint successfully deleted."
    }
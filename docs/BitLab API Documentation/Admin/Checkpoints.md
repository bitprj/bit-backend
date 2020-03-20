# Checkpoints

Created: Dec 15, 2019 12:48 AM

Model:

- name
- instruction - some text about checkpoint
- test cases - relationship

- activity
- activity_id

Inherited models

**OKCheckpoint**

- number of correct test cases
- number of incorrect test cases

**Image checkpoint**

- image to recieve - image to be graded

**Video checkpoint**

- video_to_recieve - video to be graded

**GET** FetchCheckpoint - `api.bitproject.org/activities/{{checkpoint_id}}`

This call is used to fetch a checkpoint from the database. It returns, the name and contentful_id

    {
        "id": 2,
        "contentful_id": "314mbPmZrG4K8oo1NtjL8E",
        "name": "Checkpoint 2"
    }

**POST** CreateCheckpoint - `api.bitproject.org/checkpoints`

This call is used to create a new checkpoint. It takes a webhook from contentful to receive the contentful id.

    {
    	"entityId": "5FYOAFlivZbPo6OWwNI3J4"
    }

**PUT**  UpdateCheckpoint - `api.bitproject.org/checkpoints`

This call is used to update an existing checkpoint . It receives the contentful id and name of the checkpoint from a wbehook and updates it in the database.

    {
      "entityId": "7Efl4rHwjSZjk34jktK810",
      "spaceId": "aq4puo31m564",
      "parameters": {
        "name": {
          "en-US": "Check delete!!!!!"
        },
        "checkpointType": {
          "en-US": "Image"
        }
      }
    }

**We use a POST request to delete data from contentful!**

**POST** DeleteCheckpoint - `api.bitproject.org/checkpoints`

This call is used to delete an existing checkpoint. It receives a contentful id from a webhook and deletes it in the backend.

    {
    	"entityId": "5FYOAFlivZbPo6OWwNI3J4"
    }

**PUT** SubmitCheckpointProgress -  `api.bitproject.org/checkpoints/{{checkpoint_id}}/submit`

This call is used to submit an image to a checkpoint progress in an activity. Takes the image or video from the user in a REQUEST BODY and adds it to S3. Marks the Checkpoint Progress as completed.

**Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.**

    // Below are examples of the different types of checkpoints and the data needed to be sent to them
    
    // Image Checkpoint. Must send an image file
    {
    	"image": "some image file"
    }
    
    // Video Checkpoint. Must send a video file
    {
    	"video": "some video file"
    }
    
    // Short Answer Checkpoint. Must send the student's respoonse to the short answer.
    {
    	"short_answer_response": "Some short answer response"
    }
    
    // Multiple Choice Checkpoint. Must send the student's respoonse to the Multiple Choice question.
    {
    	"multiple_choice_answer": "Student's multiple choice answer"
    }
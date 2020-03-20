# Activity Progress

Created: Dec 21, 2019 9:56 PM

Activity Progress Model (Association Object):

user_id - user id

activity_id - activity id

is_completed - checks if the user completed the activity. This is true if the student submits a video for the activity

is_graded - checks if the teaches has graded the activity or not

last_card_unlocked - id of the last card completed

cards_locked - list of cards that are locked

cards_unlocked - list of cards that are unlocked

grading_is_completed - boolean to tell whether or not the lab has been graded or not

video_is_completed - boolean to tell whether or not the video has been completed or not

assessments - list of assessments completed

**PUT** UpdateActivityProgress- `api.bitproject.org/activities/{{activity_id}}/progress`

Update the last card completed

**Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.**

    //if last_card_unlocked is null, then it will go to the first card
    
    {
    	"cards_unlocked" : [1,2],
    	"cards_locked" : [3,4,5,6],
    	"last_card_unlocked": "id of the last card completed"
    }

**DEL** DeleteActivityProgress- `api.bitproject.org/activities/{{activity_id}}/progress`

Delete the ActivityProgress when the lab is graded successfully. 

**Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.**

    {
    	"user_id" : 3424
    }
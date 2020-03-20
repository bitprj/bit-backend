# Learning View

Created: Dec 13, 2019 6:08 PM

**GET** FetchLab - `api.bitproject.org/lab/{lab_id}/fetch`

Initialize Learning View with title, module associated, and cards in the lab

    {
    	id: 12345,
    	lab_title: "Lab 101",
    	cards: [{
    						id: 12345,
    						card_title: "Card 1 Title", 
    						card_content: "link to aws markdown",
    					},...
    					]
    	last_card_opened: 4 // index of the card in the card list
    }

**GET** FetchProgress - `api.bitproject.org/lab/{lab_id}/progress/fetch`

- Get current status of locked and unlocked cards for navigation
- Get current number of gems
- Call after every time a card is unlocked

    {
    	unlocked_cards: [1, 2], // id of unlocked and locked hints
    	locked_cards: [3, 4], // id of locked cards
    	gems: 400 //gems that user has acquired for particular lab
    }

**PUT** UnlockCard - `api.bitproject.org/lab/{lab_id}/card/{card_id}/unlock`

- Update Boolean is_unlocked
- Update current gems amount

    //call
    {
    	id: 3123 // id of the next card
    }
    
    // return 
    {
    	is_unlocked: "true" // boolean to tell whether or not the next card is unlocked or not
    }

**GET** FetchCardStatus - `api.bitproject.org/lab/{lab_id}/card/{card_id}/fetch`

- Return list of unlocked and locked hints associated with a card
- Call this every time a hard card is loaded to get up to date info about locked/unlocked hints.

    {
    	id: 45678
    	gems: 100,
    	unlocked_hints: [1, 2], // id of all unlocked hints
    	locked_hints: [3, 4] // ids of all locked hints
    }

**PUT** UnlockHint - `api.bitproject.org/lab/{lab_id}/card/{card_id}/hint/{hint_id}/unlock`

This call should change the boolean `isUnlocked` from true to false

    {
    	id: 435234, // id hint
    	gem_adjustment: -10, //adjustment needed to be made to gem value
    	content: "link to aws hint markdown"
    }

**GET** FetchHint - `api.bitproject.org/lab/{lab_id}/card/{card_id}/hint/{hint_id}/fetch`

This call should return the unlocked hint or locked hint based on the boolean `isUnlocked`

    // if hint is locked
    {
    	id: 3,
    	isUnlocked : "false",
    	title: "What is Python?",
    	gems: -10
    }
    
    // else 
    {
    	id: 1,
    	isUnlocked : "true",
    	hint_title: "Why do we code?",
    	content: "link to aws hint markdown",			
    	gems: -10, 
    	type: "medium", // or "easy"
     }

**GET** FetchModal - `api.bitproject.org/lab/{lab_id}/card/{card_id}/modal`

- This call should return whether or not a card has a modal or not
- If true, then return data modal, if not move on to next card.

    //assessment
    {
    	id: 3,
    	needs_modal: "true",
    	type : "assessment",
    	assessment_type : "Multiple Choice",
    	mc_data: {
    		question: "Where can I get food",
    		choices: ["1", "2", "3", "4"],
    		correct_answer: "1"
    	}
    }
    
    //file upload
    {
    	id: 4,
    	needs_modal: "true",
    	type: "file_uploading"
    }
    
    //concept
    {
    	needs_modal: "true",
    	type : "concept",
    	"concepts": [{
    						id: 1,
    						concept_title: "Concept Title", 
    						concept_content: "Concept Text",
    						concept_right_image: "link to image"
    					}
    		]
    }
    

**PUT** Modal Response - `api.bitproject.org/modal/{modal_id}/type/{modal_type}/put`

- This call used to record the modal response

    // If the modal is a multiple choice assessment send this data
    {
    	id: 3,
    	type: "Assessment",
    	assessment_type: "Multiple Choice",
    	user_answer: "1"
    }
    
    // If modal is file uploading
    {
    	id: 4,
    	type: "File",
    	file: "file to upload" // file that the user is uploading
    }
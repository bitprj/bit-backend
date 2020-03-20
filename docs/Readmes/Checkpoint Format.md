# Checkpoint Format

## Name of the file

For the file name, name it the card that you want it to be associated with with "-checkpoint.md". So if you wanted to create a checkpoint for 1.md, you would name the checkpoint file "1-checkpoint.md"

## Name (This is required)

This is the name of the checkpoint. Put the word name in a markdown h1 tag. Put the name of the checkpoint under the h1 tag like so:

    # name
    Code Check in

## Cards Folder (This is required)

This is the folder on where the cards are located. Put the word cards_folder in a markdown h1 tag. Put the card folder path under the h1 tag like so:

    # cards_folder
    Topic1/Module7/Activity_13/cards/

## Checkpoint Type (This is required)

This is to define the type of checkpoint. Put the word checkpoint_type in a markdown h1 tag.

Checkpoints could be **ONE** of the following:

- Video
- Image
- Short Answer
- Multiple Choice
- Autograder

    # checkpoint_type

## Instruction (This is required)

This is what you would tell the user to do for a checkpoint. Put the word instruction in a markdown h1 tag. Put the instruction content under the h1 tag like so:

    # instruction
    Submit a photo your Minsweeper code working

# Optional Fields

## Criteria (This is required for Video and Image Checkpoints)

Criteria is a rubric for TA's to grade a student's Image or Video Checkpoint.

You must declare where the criteria for a checkpoint would begin. You would do this by putting the words criteria in a markdown h1 tag like so:

    # criteria

After that you can list each criteria in a  markdown h2 tag with a number at the end like so:

    ## criteria_1
    Does the student's board look like this:

## Multiple Choice (This is required for Multiple Choice Checkpoints)

You must declare where the choices for the checkpoint would begin. You would do this by putting the words mc_choices in a markdown h1 tag like so:

    # mc_choices

Next you would define each choice in a markdown h2 tag with a number at the end like so:

    ## choice_1

## Test file location (This is required for Autograder Checkpoint)

This field is used to tell where the test case folder is for the checkpoint.

    # test_file_location
    Topic1/Module7/Activity_13/Tests/test_1

# Examples

## Video/Image

    # name
    Code Check in
    
    # cards_folder
    Topic1/Module7/Activity_13/Cards/
    
    # checkpoint_type
    Video
    
    # instruction
    Submit a photo your Minsweeper code working
    
    # criteria
    
    ## criteria_1
    Does the student's board look like this?
    
    ## criteria_2
    Does the student's code print the board out?

## Short Answer

    # name
    Print Statements Short Answer
    
    # cards_folder
    Topic1/Module7/Activity_13/Cards/
    
    # checkpoint_type
    Short Answer
    
    # instruction
    Submit a photo your Minsweeper code working

## Multiple Choice

    # name
    Print Statement Multiple Choice
    
    # cards_folder
    Topic1/Module7/Activity_13/Cards/
    
    # checkpoint_type
    Multiple Choice
    
    # instruction
    Which of the following choices is the correct way to use a print statement in python
    
    # mc_choices
    
    ## choice_1
    console.log()
    
    ## choice_2
    print()
    
    ## choice_3
    printf()
    
    # correct_choice
    print()

## Autograder

    # name
    Autograder Checkpoint  
    
    # cards_folder
    Topic1/Module7/Activity_13/Cards/
    
    # checkpoint_type
    Autograder
    
    # instruction
    Do this     
    
    # test_file_location
    Topic1/Module7/Activity_13/Tests/test_1
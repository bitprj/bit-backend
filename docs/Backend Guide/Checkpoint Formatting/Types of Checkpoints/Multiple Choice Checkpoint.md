# Multiple Choice Checkpoint

Created: Feb 06, 2020 2:14 PM

**Note: Multiple Choice Checkpoints are different from the other checkpoints. You have to create a multiple choice question model and its choice models. Multiple choice questions are in Multiple Choice Checkpoints.**

Multiple choice checkpoints are to quiz whether or not the student understands the material. 

**Multiple Choice Checkpoint Fields:**

**Name**: Name of the checkpoint

**Instruction**: This is what you will tell the user to do

**Type:** This is used to indicate the type of checkpoint. For this case, it would be Multiple Choice

**Multiple Choice Question Fields:**

**Description**: The question to ask the user

**Choices**: The list of choices for the multiple choice question

**Correct Choice:** The correct answer to the question

**Choice Field:**

**Content:** The content of the choice

### Example of Multiple Choice Checkpoint

**Name**: For loop Multiple Choice Question

**Instruction**: Answer the following question

**Type:** Multiple Choice

### Example of Multiple Choice Question

**Description:** Which of the following is the correct way to write a for loop in Python to iterate from 1 to 20?

**Choices:** 

    for i in range(20):
    	#do stuff

    for num in nums:
    	#do stuff

    while True:
    	#do stuff

**Correct Choice:**

    for i in range(20):
    	#do stuff
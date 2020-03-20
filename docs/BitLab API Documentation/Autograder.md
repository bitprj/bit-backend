# Autograder

**POST** Obtain Grade results -`https://darlene-autograder.herokuapp.com/uploader`

    // Autograder checkpoint. Must send a src zip file and a tests zip file. src contains the student's code and tests contains the test cases for the activity. src zip file must be named "src.zip" and tests zip file must be named "tests.zip". If the program relies on user input, include two additional files for handling input, "input.py" which contains the overridden input() function and "input.txt" which contains the user input.
    {
    	"src": "src.zip",
    	"tests": "tests.zip"
    }

Obtain which tests in `tests_zipfile` passed and which test was the first to fail as well as their expected vs actual outputs if they fail

## Example

[src.zip](Autograder/src.zip)

[thing.py](Autograder/thing.py)

Request body must have 2 zip files:

1. "src.zip" - contains the source files (no sub directories and files must end in .py)

**Note: Do not put the code in a folder called src. Zip up the code and rename the zip file src.zip**

Example of a source file inside `src.zip`:

    def mult_add(num1, num2):
        return num1 * num2

2.   "tests.zip" - contains the test files **(files must end in .test)**

**Note: Do not put the test cases in a folder called tests. Zip up all the test cases and rename it tests.zip**

Example of a test file inside `tests.zip`: 

    # This is test1.test
    # You MUST type >>> like in the Python command prompt since okpy will run this character by character
    >>> mult_add(3, 4)
    12
    # Right after the function call, you must put the answer with no new line

## Example of JSON output

    {
      "pass_cases": [
        {
          "name": "TODO",
          "output": [
            ">>> from thing import *",
            ">>> mult_add(3, 0)",
            "0"
          ]
        },
        {
          "name": "TODO",
          "output": [
            ">>> from thing import *",
            ">>> mult_add(3, -4)",
            "-12"
          ]
        },
        {
          "name": "TODO",
          "output": [
            ">>> from thing import *",
            ">>> mult_add(3, 4)",
            "12"
          ]
        }
      ],
      "fail_case": {},
      "num_fail": 0,
      "num_pass": 3
    }
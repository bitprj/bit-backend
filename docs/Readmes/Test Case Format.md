# Test Case Format

**Note: All test case files must end with .test**

## File formating

If you have multiple test cases they should have a number at the end of it like below:

- test1.test
- test2.test
- test3.test

If you have input files, then make sure that their name as .txt. They should be in numerical order as like:

- input1.txt
- input2.txt
- input3.txt

## Name

Give the test case a name at the top of file like so:

    Testing the Create Board Function

## Inputs

To write test cases, you must type ">>>" followed by the name of the function that you wish to test on. Since you will mostly be testing the main function it would look like the following:

    >>> main()

## Outputs

Right after the declaring the function that you want to test, you would put the output right below it like so:

    >>> main()
    Hello World!

## Handling User Input

If your program needs user input, then you must include the following Python file:

[input.py](Test%20Case%20Format/input.py)

Next you must include an input.txt that specifies the user input that you want to test on. 

Imagine this is an input file where the program expects to take in color as an input

    red
    blue
    green

## Minesweeper Example

Below is the minesweeper1.test file. In this case we target the main function while passing the number 2 to it. Below that function, the output is the board and a prompt for the user input. 

    Testing the Create Board Function
    >>> main(2)
    Mines: 10
      0123456789
    0 XXXXXXXXXX 0
    1 XXXXXXXXXX 1
    2 XXXXXXXXXX 2
    3 XXXXXXXXXX 3
    4 XXXXXXXXXX 4
    5 XXXXXXXXXX 5
    6 XXXXXXXXXX 6
    7 XXXXXXXXXX 7
    8 XXXXXXXXXX 8
    9 XXXXXXXXXX 9
      0123456789
    Enter your move (for help enter "H"): 42
    Mines: 10
      0123456789
    0 XXXXXXXXXX 0
    1 XXXXXXXXXX 1
    2 XXXXMXXXXX 2
    3 XXXXXXXXXX 3
    4 XXXXXXXXXX 4
    5 XXXXXXXXXX 5
    6 XXXXXXXXXX 6
    7 XXXXXXXXXX 7
    8 XXXXXXXXXX 8
    9 XXXXXXXXXX 9
      0123456789
    Uh oh! You blew up!

Since the Minesweeper lab needs to have the input of 42, all we have to do is create an input1.txt with 42 in it. **Do not put a new line if your program does not output a newline.**

    42
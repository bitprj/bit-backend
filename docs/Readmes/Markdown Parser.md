# Markdown Parser

## How Parser works

The parser uses headings as JSON keys and the content below it would be the value associated with that key. 

The parser would see the heading below and make that the key in JSON. The content below would be the value associated with Description.

    # Description
    Some description

The parser would transform that markdown snippet above to this:

    {
    	"Description": "Some description"
    }

## Arrays

The parser looks for * to indicate that the listed elements are in an array. 

You still have to declare a key for the array to be associated with like so:

    # Activities

Next you can each element in with a star next to it like so:

    # Activities
    
    * Minsweeper
    * Battleship
    * nColorable

The output would be:

    {
    	"Activities": ["Minesweeper", "Battleship", "nColorable"]
    }

## Object within an Object

To associate an object with an Activity you must use lower order headers for the object. 

This our key in a markdown heading 1 tag

    # Activity

If we want to assign Activity to an object we must use markdown heading 2 tags for the rest of the data like so:

    # Actvitiy
    
    ## name
    Minesweeper
    
    ## description
    Some description

In the end the markdown would be parsed to:

    {
      "Activity": {
        "name": "Minsweeper",
        "description": "Some description"
      }
    }

## Package used to parse MD to JSON

[njvack/markdown-to-json](https://github.com/njvack/markdown-to-json)
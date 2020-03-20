# Activity/Lab README

## Github id (This is required)

Each activity needs a github_id so that the server knows it is unique.

    # github_id
    1

## Name (This is required)

Each Activity needs a name field. The name should be in markdown h1 tag like below:

    # name
    Some Activity

## Description (This is required)

Each Activity has a description field to describe what the activity will accomplish. The description should be in markdown h1 tag like below:

    # description
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip.

## Summary (This is required)

Each Activity has a summary field to describe what the activity will accomplish in depth. The summary should be in markdown h1 tag like below:

    # summary
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum 

## Difficulty (This is required)

Each Activity/Lab needs a Difficulty field to indicate how hard the Activity/Lab is for the user. Add the word difficulty in a markdown h1 tag, and put the difficulty under it:

Types of Difficulty:

- Hard
- Medium
- Easy

    # difficulty
    Hard

## Image (This is required)

Each Activity has an image field. The image should be in markdown h1 tag like below:

    # image
    <img src="images/bandanna.jpg">

## Image Folder (This is required)

Each Activity needs to point to an image folder where the image is being used. The image_folder should be in a markdown h1 tag like below:

    # image_folder
    Topic1/Module2_test/Activity_4/

## Cards

The cards fields is used to indicate the name of the card, order in which the card is shown and number of gems that the card has.

### Cards (This is required)

To define cards in an Activity, you have to first cards in a markdown h1 tag. This is used to tell the server where the cards are:

    # cards

### Card Key (This is required)

Each card you define in the Activity README, must have a corresponding filename as its key. For example if a card/hint was named [1.md](http://1.md) then its key would be 1. The card key must be placed in a markdown h2 tag like below:

    ## 1

### Card Name (This is required)

Each card has a name field. Each name should be in a markdown h3 tag like below: 

    ### name
    Card 1 Github

### Card Order (This is required)

Each card has a order field. The order is the last digit of the card key. If a card had a key of 1-2, then the order for that card would be 2. The order of a card is the order in which each card is displayed. Each name should be in a markdown h3 tag like below: 

    ### order
    2

### Card Gems (This is required)

Each card has a gems field. The gems fields is used to indicate the number of gems earned when opening a card. Each name should be in a markdown h3 tag like below: 

    ### gems
    300

**Note: When defining the cards, please put them in order of difficulty. Hard cards should be defined first, Medium cards next, and last easy cards. Below is an example:**

    # cards
     
    ## 1
    
    ### name
    Bleh Card 1 Github
    
    ### order
    1 
    
    ### gems
    300
    
    ## 2
    
    ### name
    Bleh Card 2 Github
    
    ### order
    2
    
    ### gems
    300
    
    ## 1-1
    
    ### name
    Bleh Card 2 Github
    
    ### order
    1
    
    ### gems
    300
    
    ## 2-1
    
    ### name
    Bleh Card 4 Github
    
    ### order
    1
    
    ### gems
    300
    
    ## 1-1-1
    
    ### name
    Bleh Card 3 Github
    
    ### order
    1
    
    ### gems
    300
    
    ## 1-2-1
    
    ### name
    Bleh Card 4 Github
    
    ### order
    1
    
    ### gems
    300
    
    ## 2-1-1
    
    ### name
    Bleh Card 131 Github
    
    ### order
    1
    
    ### gems
    300

## Final Example

    # github_id
    19
    
    # name
    Some Activity
    
    # description
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip.
    
    # summary
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum 
    
    # difficulty
    Hard
    
    # image
    <img src="images/bandanna.jpg">
    
    # image_folder
    Topic1/Module2_test/Activity_4/
    
    # cards
    
    ## 1
    
    ### name
    Card 1 Github
    
    ### order
    2
    
    ### gems
    300
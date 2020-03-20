# Topic README

## Github id (This is required)

Each topic needs a github_id so that the server knows it is unique.

    # github_id
    1

## Name (This is required)

Each Topic needs a name field. The name should be in markdown h1 tag like below:

    # name
    Postman Topic

## Description (This is required)

Each Topic has a description field to describe what the topic will accomplish. The description should be in markdown h1 tag like below:

    # description
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum 

## Image (This is required)

Each Topic has an image field. The word image should be in markdown h1 tag while the image url should be put in an img tag:

    # image
    <img src="images/dee.jpg">

## Image Folder (This is required)

Each Topic needs to point to an image folder where the image is being used. The image_folder should be in a markdown h1 tag like below:

    # image_folder
    /Topic_Postman/

## Modules (This is not required)

Each Topic has modules. To add modules to a topic, add the module's github_ids in a list. Add the word modules in a markdown h1 tag and then add the github_ids in a list with *'s:

    # modules
    * 5

## Final Example

    # github_id
    1
    
    # name
    Postman Topic
    
    # description
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum  
    
    # image
    <img src="images/dee.jpg">
    
    # image_folder
    /Topic_Postman/
    
    # modules
    * 5
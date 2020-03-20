# Concept Format

## Concept Name (You need to include this for each Concept)

Each concept needs a name. The name should be in a h1 tag like below:

    # concept_name
    Concept name

### Image Folder (You need to include this for each Concept)

Each Concept needs to point to an image folder where the image is being used. The image_folder should be in a markdown h1 tag like below: (**Note: since we are still using S3 you can omit the image_folder for now**)

    # image_folder
    Topic1/Module2_test/concepts/

### Step Key (You need to include this for each step)

Next you **must** include the step key so the server can keep track of the steps. The Step key should be the concept name along with the step number in a markdown h1 tag like this:

    # concept_name Step 1

### Step name (You need to include this for each step)

Under the hint name, you have to give the step a name with a markdown h2 tag. **Please put the contents of name in a code block.** It should look something like this:

    ## name
    ```
    How to install VSCode
    ```

### Md_content (You need to include this for each step)

To include the md_content for the step, give the md_content with a markdown h2 tag. **Please put the contents of md_content in a code block.** It should look something like this:

    ## md_content
    ```
    # Hello world in js
    This is how you do **it**
    ```

# Optional Fields

### Code Snippet

To include the code snippet for the step, give the code snippet with a markdown h2 tag. **Please put the contents of the code in a code block.** It should look something like this:

    ## code_snippet
    ```
    def pls_work():
        return True... maybe
    ```

### Image

To include an image for a step, you need to put a h2 markdown tag and assign it to "image"

    ## image
    <img src="dee.jpg">

## Final Example:

Note: You can always add more hint as long as you follow the above syntax.

    # image_folder
    Topic1/Module2_test/concepts/
    
    # 1-2-1 Step 1
    
    ## name
    ```
    How to install VSCode
    ```
    
    ## md_content
    ```
    # Hello world in js
    This is how you do **it**
    ```
    
    ## code_snippet
    ```
    def pls_work():
        return True... maybe
    ```
    
    ## image
    <img src="dee.jpg">
# Build Track Model

Date Created: Dec 16, 2019 12:54 AM
Property: Bryan Wong
Status: Done 🙌

Things to add to Topic model and Schema:

- description - string
- image - string
- topics - many to many relationship

Things to edit in [routes.py](http://routes.py) and utils.py

- Edit topic_create and topic_edit in utils to incorporate the topic model changes
- Add error validation in routes.py
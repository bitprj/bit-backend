# Concept

Created: Jan 31, 2020 9:36 PM

**Note: All concepts will be created through a CMS**

Concept model

- Concepts are ideas to help a student in an activity if they forgot certain concepts.

Concept fields

- name - name of the Concept
- contentful_id - the contentful id from cotentful
- cards - keeps track of the cards that a concept belongs to. **Many to many with Card model.**
- steps - keeps track of the steps that belong to a concept. **One to many with Step model.**
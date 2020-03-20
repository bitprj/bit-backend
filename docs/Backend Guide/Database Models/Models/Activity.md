# Activity

Created: Jan 31, 2020 5:02 PM

**Note: All activities will be created through a CMS**

Activity model

- Keeps track of the material that a student would be learning

Activity fields

- name - name of the activity
- contentful_id - the contentful id from cotentful
- cards - the cards associated with an activity. **One to many with Card model.**
- modules - keeps track of the modules that the activity belongs to. **Many to many with Module model.**
- module_prereqs - keeps track of all of the modules that an activity is a prerequisite to it. **Many to many with Module model.**
- badge_prereqs - keeps track of all the badge xp needed to access an activity. **Many to many with ActivityBadgePrereqs**
- badge_prereqs - keeps track of all the badge xp needed to access an activity. **Many to many with ActivityBadgePrereqs**
- students_complete - keeps track of the students that completed an activity. **Many to many with Student model.**
- students_incomplete - keeps track of the students that have not completed an activity. **Many to many with Student model.**
- students_current - keeps track of the students that are currently working on an activity. **Many to many with Student model.**
- topics - keeps track of the topics that an activity is a prerequisite to it. **Many to many with Topic model.**
# Student

Created: Jan 31, 2020 5:06 PM

Student model

- Students are the users who completes activities

Student fields

- incomplete_activities - the activities that are not completed by the student. These are the activities needed to complete a track. **Many to many with Activity model.**
- completed_activities - the activities that are completed by the student. **Many to many with Activity model.**
- current_activities - the activities that the student is currently working on. **Many to many with Activity model.**
- incomplete_modules - the modules that are not completed by the student. **Many to many with Module model.**
- completed_modules - the modules that are completed by the student. **Many to many with Module model.**
- inprogress_modules - the topics that the student is currently working on. **Many to many with Module model.**
- incomplete_topics - the topics that are not completed by the student. **Many to many with Topic model.**
- completed_topics - the topics that are completed by the student. **Many to many with Topic model.**
- inprogress_topics - the topics that the student is currently working on. **Many to many with Topic model.**
- current_track - the track that the student is currently working on. **One to many with Track model.**
- activity_progresses - this keeps track of the progress of each activity that the student is working on. **One to many with ActivityProgress model.**
- classes - this keeps track of which classrooms that the student belongs to. **Many to many with Classroom model.**
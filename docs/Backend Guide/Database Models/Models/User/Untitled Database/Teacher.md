# Teacher

Created: Jan 31, 2020 5:06 PM

Teacher model

- The role of a teacher is to grade a student's activities
- Has special access to routes that only a teacher can visit
- A teacher is not allowed to view a classroom that they do not own

Teacher fields

- classrooms - keeps track of the classrooms that a teacher owns. **Many to many with Classroom model.**
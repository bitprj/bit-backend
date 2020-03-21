# API Suggestions

### GET FetchProgress

Probably no longer need since:

- lock/unlock status of cards can be deduced from 'last_card_unlock' of FetchLab.
- total number of gems can just be returned in FetchLab.

### POST Login

Should return what type the user is (student, teacher, or admin) alongside token and message.

### GET Fetch(Student/User)Info

There should be an API call to fetch student/user general info (name, class, currentLabID, currentTopicID, currentTrackID,...) after authentication.
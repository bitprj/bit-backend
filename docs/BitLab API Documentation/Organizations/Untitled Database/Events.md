# Events

Created: Feb 10, 2020 10:27 PM

**Event Model**

name - name of the Event

image - image for organization

background_image

is_active - Boolean to check if the organization is active

owners - List of users who own the organization

active_users - List of users who are active in the organization

inactive_users - List of users who are inactive in the organization

events - List of events that are hosted by the organization

**GET** FetchEvent - `api.bitproject.org/events/{{event_id}}`

This call is used to fetch an event based on the event_id.

    {
        "name": "Oz KBBQ meetup",
        "date": "2018-12-05",
        "summary": "Lets all get KBBQ",
        "location": "Elk Grove",
        "organization": {
            "id": 1,
            "name": "HotPot Gang"
        },
        "presenters": [
            {
                "username": "Student@example.com"
            },
            {
                "username": "d2048220@urhen.com"
            }
        ],
        "rsvp_list": [
            {
                "username": "Student@example.com"
            },
            {
                "username": "d2048220@urhen.com"
            }
        ]
    }

**POST** CreateEvent - `api.bitproject.org/{{url}}/events/create`

This call is used to create an event.

Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript

    {
        "message": "Event successfully created"
    }

**PUT** UpdateEvent - `api.bitproject.org/{{url}}/events/{{event_id}}`

This call is used to update an Event.

Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript

    {
        "message": "Event successfully updated"
    }

**DELETE** DeleteEvent - `api.bitproject.org/{{url}}/events/{{event_id}}`

This call is used to delete an Event.

Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript

    {
        "message": "Event successfully deleted"
    }

**PUT** JoinEvent - `api.bitproject.org/{{url}}/events/{{event_id}}/rsvp`

This call is used to let a user rsvp for an envent.

Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript

    {
        "message": "Student has RSVP'd for Oz KBBQ meetup"
    }

**DELETE** LeaveEvent - `api.bitproject.org/{{url}}/events/{{event_id}}/rsvp`

This call is used to let a user leave the RSVP list for an event.

Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript

    {
        "message": "Successfully left the RSVP list"
    }
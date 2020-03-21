# Organizations

Created: Feb 10, 2020 10:27 PM

**Organization Model**

name - name of the organization

image - image for organization

background_image

is_active - Boolean to check if the organization is active

owners - List of users who own the organization

active_users - List of users who are active in the organization

inactive_users - List of users who are inactive in the organization

events - List of events that are hosted by the organization

**GET** FetchOrganization - `api.bitproject.org/organizations/{{organization_id}}`

This call is used to fetch a organization based on id.

    {
        "name": "HotPot Gang",
        "image": "https://projectbit.s3-us-west-1.amazonaws.com/darlene/organizations/Image%20from%20iOS.jpg",
        "background_image": "https://projectbit.s3-us-west-1.amazonaws.com/darlene/organizations/Image%20from%20iOS.jpg",
        "owners": [
            {
                "username": "Student@example.com"
            }
        ],
        "active_users": [
            {
                "username": "d2048220@urhen.com"
            }
        ],
        "inactive_users": []
    }

**POST** CreateOrganization - `api.bitproject.org/{{url}}/organizations/create`

This call is used to create a organization.

Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.

You must send the data in FormData.

    {
        "message": "Organization successfully created"
    }

**PUT** UpdateOrganization - `api.bitproject.org/{{url}}/organizations/{{organization_id}}`

This call is used to update the organization details.

Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.

    {
        "message": "Organization successfully updated"
    }

**DELETE** DeleteOrganization - `api.bitproject.org/{{url}}/organizations/{{organization_id}}`

This call is used to delete a organization.

Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.

    {
        "message": "Organization successfully deleted"
    }

**PUT** InviteOwners - `api.bitproject.org/{{url}}/organizations/{{organization_id}}/invite`

This call is used to invite users to become owners in an organization.

Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.

    {
        "message": "Invites have been sent"
    }

**DELETE** RemoveMember - `api.bitproject.org/{{url}}/organizations/{{organization_id}}/remove`

This call is used to remove a user from an organization. This is only usuable by owners of an organization.

Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.

    {
        "message": "Removed random from HotPot Gang"
    }

**PUT** JoinOrganization - `api.bitproject.org/{{url}}/organizations/{{organization_id}}/membership`

This request is used to let users join organizations

Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.

    {
        "message": "random has joined HotPot Gang"
    }

**DELETE** LeaveOrganization - `api.bitproject.org/{{url}}/organizations/{{organization_id}}/membership`

This call is used for a user to leave an organization.

Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.

    {
        "message": "You successfully left HotPot Gang"
    }
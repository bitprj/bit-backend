# Grading

Created: Jan 04, 2020 5:55 PM

**GET**  FetchSubmissions - `api.bitproject.org/teachers/{{classroom_id}}/grade`

This call is used to get all the ready to grade assignments for their classroom.

    [
        {
            "id": 31,
            "student": {
                "name": "Student 3"
            },
            "activity": {
                "name": "Testingd"
            },
            "checkpoints": [
                {
                    "checkpoint_id": 38,
                    "is_completed": true,
                    "image_to_receive": "https://projectbit.s3-us-west-1.amazonaws.com/darlene/checkpoints/Image%20from%20iOS.jpg",
                    "video_to_receive": null,
                    "checkpoint": {
                        "checkpoint_type": "Image"
                    }
                },
                {
                    "checkpoint_id": 39,
                    "is_completed": true,
                    "image_to_receive": "https://projectbit.s3-us-west-1.amazonaws.com/darlene/checkpoints/Image%20from%20iOS.jpg",
                    "video_to_receive": null,
                    "checkpoint": {
                        "checkpoint_type": "Image"
                    }
                },
                {
                    "checkpoint_id": 40,
                    "is_completed": true,
                    "image_to_receive": null,
                    "video_to_receive": null,
                    "checkpoint": {
                        "checkpoint_type": "Video"
                    }
                }
            ]
        }
    ]

**PUT**  GradeActivity - `api.bitproject.org/teachers/{{classroom_id}}/grade`

Marks checkpoint submissions. Submit checkpoint progress ids along with their optional comment.

**Need to include X-CSRF-TOKEN in this request. You can extract it from the csrf_access_token. It is readable from Javascript.**

    // This is what that front end will send to the backend
    {
        "activity_progress_id": 31,
        "checkpoints_passed": [
            {
                "id": 38,
                "comment": "blah"
            },
            {
                "id": 39,
                "comment": "blah blah"
            }
        ],
        "checkpoints_failed": [
            {
                "id": 40,
                "comment": "Bad video"
            }
        ]
    }
# User

Created: Dec 14, 2019 12:19 PM

**GET** FetchGlobalGems - `api.bitproject.org/user/data/gems`

Get the total number of gems associated with a student

    {
    	gems: 100
    }

**GET** FetchForkedLabs - `api.bitproject.org/user/data/forked`

Get the total number of forked labs done by student

    {
    	forked: 100
    }

**GET** FetchActivity - `api.bitproject.org/user/data/labs`

Get the total number of labs done by student

    {
    	labs: 100
    }

**GET** FetchStreak - `api.bitproject.org/user/data/streaks`

Get the total number of days continuous done by student

    {
    	streak: 3
    }

**GET** FetchBadges - `api.bitproject.org/user/data/badges`

    {
    	badges: [{
    						id: 12345,
    						badge_icon: "badge_icon_png_url",
    						badge_title: "Software Engineering",
    						badge_level: 1,
    						badge_exp: 300,
    						badge_threshold: 500
    					}
    					]
    }

**GET** FetchTrack - `api.bitproject.org/user/data/track`

    {
    	id: 
    	track: Computer Science
    
    }
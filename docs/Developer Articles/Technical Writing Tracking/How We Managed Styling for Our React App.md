# How We Managed Styling for Our React App

Assigned: Daniel Kim
Status: Writing

At Bit Project, we are building a large react app to teach our students coding and software engineering. However, we quickly realized in order to maintain continuity among our many screens, we have to have a good foundation for the styling of our application. 

In this article, I will introduce a very high level overview of managing styling for a large React app.

**How we fucked up**

It's hard to admit, but our first crack at our app was a mess. There was random styling everywhere and there was conflicting styling everywhere. Having a spaghetti of CSS files meant we spent hours and hours messing with the existing css with the eventual result having our apps load ever more slower. In addition, teams will feel frustrated as they’ll be forced to remove the technical debt while still iterating on user-facing features.
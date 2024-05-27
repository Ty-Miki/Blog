# Django Blog Application

This is a blog application built with **django**.

It has *one data model* to store blog posts, *two views* to render posts in list view and detail view and *templates* for each.

I have used **tailwind CSS** to style webpages.

## Instructions

- First you have to run ***python manage.py makemigrations*** to create new migration files based on defined models.
- Then run ***python manage.py migrate** to apply migrations to the database.*
- Finally run ***python manage.py runserver*** to run the django application in a local server.

## Requirements

- Requires **Python 3.12.3**
- All library dependencies are found in **req.txt**
- A .env file inside the same directory as settings.py that contains Django Secret Key and Credentials to send emails.

##### Added features in version2.0

- Added canonical URLs and used them to create SEO friendly URLs for post_detail views.
- Added pagination to post_list views to show a maximum of 5 posts per page.
- Added a feature to recomend posts through email. *this feature requires **email credentials** to be added to a .env file.*
- Added a feature to accept comments for each post.

##### Added features in version3.0

- Added a tagging feature to posts.
  - Each post is assocaued with tags, that can be used as keywords to sort recomend similar posts and search for posts containg those tags.
- Used custom template tags to show a list of latest posts and most commented posts in the sidebar.
- Used custom template filter to render markdown text.
  - This feature allows users to post blog body using markdown format.
- Added a sitemap using the sitemap framework.
- Added an RSS feed using the syndication framework.
- Changed project database into PostgreSQL to implement full-text search engine using psycopg2-binary and Django's postgres framework.

###### Added requirements

- The .env file should be updated with postgreSQL database credentials.
  - It needs to be populated with database name, database user and database password.

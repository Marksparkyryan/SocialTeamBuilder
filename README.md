# Social Team Builder

Social Team Builder is a final capstone project from the Team Treehouse Tech Degree that helps users create and apply to coding projects. Projects can have 
multiple positions, and have them linked to specific skills that are then searchable by other users. 
Users that create projects have the ability to accept or decline applicants. Applicants are notified via Django's 
messaging framework of their application outcomes. Users also have a profile that describes who they are, what 
skills they have, and what projects they have been connected to that are now completed.

Update: 
This has been deployed for demo purposes. It's running on Heroku with Gunicorn, a PostgreSQL database, and static files served by AW3. This deployment can be found at https://social-team-builder-pro.herokuapp.com


<br/>

# Features 

Development Mode
* Addition and deletion of embedded forms within forms (formsets) via JS for projects and user profiles
* Messaging of application status change on next page reload (would like to change this to asynchronous behaviour in the future)
* Token confirmation via email
* Pagination of project and application results
* Markdown capability in profile and projects
* Cropping capability for avatars
* Auto database population via data migration files

Deployment
* PostgreSQL database
* Static files served by S3

<br/>

# Cloning and Installing

1. cd into your directory of projects (or wherever you prefer to keep your clones)
2. git clone ```https://github.com/Marksparkyryan/SocialTeamBuilder.git``` to clone the app
3. ```virtualenv venv``` to create your virtual environment
4. ```source venv/bin/activate``` to activate the virtual environment
5. ```pip install -r SocialTeamBuilder/requirements.txt``` to install app requirements
6. cd into ```SocialTeamBuilder/socialteambuilder/``` (the directory with manage.py) and run ```python manage.py makemigrations``` to construct/prepare migration files
7. cd into ```SocialTeamBuilder/socialteambuilder/``` (the directory with manage.py) and run ```python manage.py migrate``` to construct and populate database (this project has a few data migration files that will inject random dummy data for users, projects, skills, and even applications)
8. cd into ```SocialTeamBuilder/socialteambuilder/``` (the directory with manage.py) and run ```python manage.py runserver```
9. the app should now be running on ```http://127.0.0.1:8000```

<br/>

# Usage

1. Register an account (token activation may be required, see settings below)
2. Fill out your profile
3. Browse current and open projects on the dashboard, seeing details by clicking on project
4. Navigate to your profile by clicking on mini avatar in header. Click Applications to see your inbox and outbox holding applications for each position. If you own a project, you can accept or decline applicants in the inbox. If you've applied to a project, you can see the application status in your outbox.
5. Projects can be created at the Dashboard (the homepage).
6. Once projects have a completed status, they will appear on your profile as work history.


<br/>

# Settings

USE_TOKEN_AUTH_WITH_DUMMY_INBOX = False

If you'd like to use the token activation feature, set USE_TOKEN_AUTH_WITH_DUMMY_INBOX to True. When True, new users need to be activated before using the site. To simulate emails, you'll have to proceed to the dummy inbox  ```SocialTeamBuilder/socialteambuilder/dummy_email_inbox/``` to copy/paste the token link in your 
browser. This should automatically activate your account and log you in. 


USE_DATA_MIGRATIONS = True

If you don't want the database to automatically populated with dummy data, set USE_DATA_MIGRATIONS to False.


<br/>

# Credits

Treehouse Techdegree Project 12 (Final Capstone Project)

Many-to-Many display of skills and the saving of additional skills is provided by:
https://django-select2.readthedocs.io/en/stable/index.html

Markdown functionality is provided by the following packages:
https://github.com/trentm/django-markdown-deux
https://pypi.org/project/django-markdown/

User registration with an email confirmation was possible by referring to the following guides:
Django registration with confirmation email, https://medium.com/@frfahim/django-registration-with-confirmation-email-bb5da011e4ef
https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html


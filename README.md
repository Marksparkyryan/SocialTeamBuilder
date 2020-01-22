# SocialTeamBuilder

Social Team Builder is a capstone project that helps users create and apply to projects. Projects can have 
multiple positions (10), and have them linked to specific skills that are then searchable by other users. 
Users that create projects have the ability to accept or decline applicants. Applicants are notified via Django's 
messaging framework of their application outcomes. Users also have a profile that describes who they are, what 
skills they have, and what projects they have been connected to that are now completed.


<br/>

# installation

1. cd into your directory of projects (or wherever you prefer to keep your clones)
2. git clone ```https://github.com/Marksparkyryan/SocialTeamBuilder.git``` to clone the app
3. ```virtualenv .venv``` to create your virtual environment
4. ```source .venv/bin/activate``` to activate the virtual environment
5. ```pip install -r SocialTeamBuilder/requirements.txt``` to install app requirements
6. cd into ```SocialTeamBuilder/socialteambuilder/``` and run ```python manage.py runserver```
7. the app should now be running on ```http://127.0.0.1:8000/accounts/register/```

<br/>

# usage

The database has been included with this repo. It contains projects, positions, skills, and users. To test out 
the site, go ahead and register for a new account. Users need to be activated so you'll have to proceed to 
the dummy inbox  ```SocialTeamBuilder/socialteambuilder/dummy_email_inbox/``` to copy/paste the token link in your 
browser. This should automatically activate your account and log you in. 

Once you've filled out your profile, you can navigate open projects and positions. You can try to apply to
any of these positions. You'll be able to see the status of your applications in your applications outbox. 
If you'd like to simulate a project owner accepting your application you can log in with the credentials below:

superuser:
email: sparky@email.com
password: securepassword

In Sparky's account, you can access applicants by going to the applications inbox. You can accept or decline 
applicants. Applicants will be notified via Django's message framework.

<br/>


# credits

Treehouse Techdegree Project 12

Many-to-Many display of skills and the saving of additional skills is provided by:
https://django-select2.readthedocs.io/en/stable/index.html

Markdown functionality is provided by the following packages:
https://github.com/trentm/django-markdown-deux
https://pypi.org/project/django-markdown/

User registration with an email confirmation was possible by referring to the following guides:
Django registration with confirmation email, https://medium.com/@frfahim/django-registration-with-confirmation-email-bb5da011e4ef
https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html


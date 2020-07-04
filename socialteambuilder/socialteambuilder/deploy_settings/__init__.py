# These are the DEPLOYMENT SETTINGS

from socialteambuilder.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECURE_HSTS_SECONDS = 600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_REFERRER_POLICY = 'same-origin'

ALLOWED_HOSTS = [
    'localhost',
    '.herokuapp.com'
]

SECRET_KEY = get_env_variable("SECRET_KEY")

# These are the DEPLOYMENT SETTINGS

import dj_database_url
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

INSTALLED_APPS.append('storages')

AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY_ID = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_env_variable("S3_BUCKET_NAME")
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

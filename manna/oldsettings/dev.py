from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6yeaqmtulfmrj&sv2&4)+@^u-)dna2d181r@ar2ok90&$obkym'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AWS_STORAGE_BUCKET_NAME = 'dev.pleromabiblechurch.org'
AWS_AUTO_CREATE_BUCKET = True

BASE_URL = 'https://dev.pleromabiblechurch.org'

try:
    from .local import *
except ImportError:
    pass

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ur-bv@^c%5xbu5#^lph$!#y4=p))&543$s$n@lfwd(#%x_3_pr'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('RDS_DB_NAME', RDS_DB_NAME),
         'USER': os.environ.get('RDS_USERNAME', RDS_USERNAME),
         'PASSWORD': os.environ.get('RDS_PASSWORD', RDS_PASSWORD),
         'HOST': os.environ.get('RDS_HOSTNAME', RDS_HOSTNAME),
         'PORT': os.environ.get('RDS_PORT', RDS_PORT),
    }
}

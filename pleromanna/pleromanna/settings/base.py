""" Django settings for pleromanna project.

Generated by 'django-admin startproject' using Django 2.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from unipath import Path

PROJECT_DIR = Path(__file__).ancestor(3)

STATICFILES_DIRS = ( PROJECT_DIR.child("assets"), )

INSTALLED_APPS = [
    'pleromanna',
    'storages',
    'search',
    'commonblocks',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.modeladmin',
    'modelcluster',
    'taggit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'pleromanna.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(PROJECT_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pleromanna.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# Wagtail settings

WAGTAIL_SITE_NAME = "pleromanna"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'

# Setup static and media file storage
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
STATICFILES_LOCATION = 'static'
STATIC_URL = '/%s/' % STATICFILES_LOCATION
MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "/%s/" % MEDIAFILES_LOCATION

if os.getenv('HOSTNAME', 'notta') != 'spade':
    AWS_DEFAULT_ACL = None
    AWS_STORAGE_BUCKET_NAME = "www.pleromabiblechurch.org"
    AWS_S3_CUSTOM_DOMAIN = 's3-us-east-2.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = { 'CacheControl': 'max-age=86400', }
    AWS_S3_FILE_OVERWRITE = False

    STATICFILES_STORAGE = 's3_storage.StaticStorage'
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

    DEFAULT_FILE_STORAGE = 's3_storage.MediaStorage'
    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

print("static storage at {}".format(STATIC_URL))
print("media storage at {}".format(MEDIA_URL))
CSRF_TRUSTED_ORIGINS=['.pleromabiblechurch.org']

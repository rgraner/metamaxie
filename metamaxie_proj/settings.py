"""
Django settings for metamaxie_proj project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    # My apps
    'scholarships',
    'tasks',
    'payments',
    'users',
    'profiles',

    # 3rd part apps
    'bootstrap5',
    'crispy_forms',
    'mathfilters',

    # Default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'metamaxie_proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'scholarships.context_processor.total_slp',
            ],
        },
    },
]

WSGI_APPLICATION = 'metamaxie_proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR/'static']
# STATIC_ROOT = BASE_DIR/'staticfiles'

# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR/'media'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

if DEBUG:
  STATICFILES_DIRS = [BASE_DIR/'static']
else:
  STATIC_ROOT = BASE_DIR/'staticfiles'

MEDIA_ROOT = BASE_DIR/'media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# My settings
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL ='/'
LOGOUT_REDIRECT_URL ='users:login'

AUTH_USER_MODEL = 'users.User'

#SMTP configuration
# EMAIL_HOST = os.environ.get('SENDGRID_EMAIL_HOST')
# EMAIL_HOST_USER = os.environ.get('SENDGRID_EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')
# EMAIL_PORT = os.environ.get('SENDGRID_EMAIL_PORT')
# EMAIL_USE_TLS = os.environ.get('SENDGRID_EMAIL_USE_TLS')
# DEFAULT_FROM_EMAIL = os.environ.get('SENDGRID_DEFAULT_FROM_EMAIL')

EMAIL_HOST='smtp.sendgrid.net'
EMAIL_HOST_USER='apikey' # this is exactly the value 'apikey'
API_KEY='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'
EMAIL_PORT=465
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL='admin@metamaxie.com'


# Heroku settings.
if DEBUG:
    import django_heroku
    django_heroku.settings(locals())

    if os.environ.get('DEBUG') == 'TRUE':
        DEBUG = True
    elif os.environ.get('DEBUG') == 'FALSE':
        DEBUG = False

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    #SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    #SECURE_SSL_REDIRECT = True




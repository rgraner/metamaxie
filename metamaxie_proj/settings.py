"""
Django settings for metamaxie_proj project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k#%+r%ur232y6axxjg$#vo!68hxe5_n$i@tq8&v4=!vrgt9$vl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['metamaxie.herokuapp.com', '127.0.0.1']

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
        'NAME': 'metamaxie_db',
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
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'metamaxie21@gmail.com'
EMAIL_HOST_PASSWORD = 'jk\sdhfgudk@utf'

# Heroku settings.
if DEBUG:
    import django_heroku
    django_heroku.settings(locals())

    import os
    if os.environ.get('DEBUG') == 'TRUE':
        DEBUG = True
    elif os.environ.get('DEBUG') == 'FALSE':
        DEBUG = False

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'




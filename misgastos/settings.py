"""
Django settings for misgastos project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import django_heroku
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
STATIC_DIR = os.path.join(BASE_DIR,'static')
#STATIC_ROOT = STATIC_DIR

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i=5iz!5uit12_7id%4jl&5_ht!=+3o%$6d3u*a)nebwo^+!p_='

# SECURITY WARNING: don't run with debug turned on in production!

if os.environ['HOME'] == '/home/cristhian':
    DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1']
    STATIC_ROOT = '/home/ccantero86/django-misgatos/static'
elif os.environ['HOME'] == '/home/ccantero86':
    print("2")
    DEBUG = True
    ALLOWED_HOSTS = ['ccantero86.pythonanywhere.com']    
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
else:
    print("3")
    #STATIC_ROOT = '/home/ccantero86/django-misgatos/static'
    DEBUG = True
    ALLOWED_HOSTS = ['ccantero86.pythonanywhere.com','mis-presupuestos.herokuapp.com']    
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Activate Django-Heroku.
django_heroku.settings(locals())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'accountsapp',
    'categoriesapp',
    'budgetsapp',
    'expensesapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # For Heroku
]

ROOT_URLCONF = 'misgastos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
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

WSGI_APPLICATION = 'misgastos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR, ]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # For Heroku

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'thanks'

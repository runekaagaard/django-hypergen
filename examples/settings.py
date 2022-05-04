"""
Django settings for examples project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os, sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'op^-e1e2ixoo2+8qa186!2rf4f&s)*5j8f@fz0#nu0#yyc1ckd'

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get("PROD", False):
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ["*"]
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
    'django.contrib.messages', 'django.contrib.staticfiles', 'website', 'hypergen', 'todomvc', 'inputs',
    'gameofcython', 'djangotemplates', 'hellohypergen', 'hellocoreonly', 'hellocoreonly2', 't9n', 'notifications',
    'commands', 'partialload', 'hellomagic']

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware' if os.environ.get("PROD", False) else None,
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware' if not os.environ.get("CSRF_DISABLE", False) else None,
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hypergen.core.context_middleware',
    'django.middleware.cache.FetchFromCacheMiddleware' if os.environ.get("PROD", False) else None,]

MIDDLEWARE = [x for x in MIDDLEWARE if x is not None]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
    'context_processors': [
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',],},},]

# WSGI_APPLICATION = 'examples.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',}}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files to S3 with cache busting.
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3ManifestStaticStorage'
AWS_STORAGE_BUCKET_NAME = "hypergen-staticfiles"
AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_AUTH = False
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=2592000'}

# Log to stdout
if os.environ.get("PROD", False):
    LOGGING = {
        'version': 1, 'disable_existing_loggers': False,
        'formatters': {'verbose': {'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}}, 'handlers': {
        'console': {'level': 'INFO', 'class': 'logging.StreamHandler', 'stream': sys.stdout,
        'formatter': 'verbose'}}, 'loggers': {'': {'handlers': ['console'], 'level': 'INFO', 'propagate': True}}}

"""
Minimal settings for basic deployment
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-minimal-deployment-key-12345')

DEBUG = False

ALLOWED_HOSTS = ['*']  # Allow all hosts for initial deployment

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'chatbot_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'chatbot_project.minimal_urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
    },
]

WSGI_APPLICATION = 'chatbot_project.wsgi.application'

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Disable database for minimal deployment
USE_TZ = False
DATABASES = {}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""
Ultra minimal settings for basic deployment - no dependencies
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-minimal-key-for-deployment-only'

DEBUG = False

ALLOWED_HOSTS = ['*']

# Absolutely minimal apps - no database, no auth
INSTALLED_APPS = [
    'django.contrib.staticfiles',
]

# Minimal middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'chatbot_project.ultra_minimal_urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

WSGI_APPLICATION = 'chatbot_project.wsgi.application'

# No database at all
USE_TZ = False
DATABASES = {}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import os 
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = [
    'halogen-delay-uncharted.ngrok-free.dev', # URL do seu túnel ngrok
    '127.0.0.1', 
    'localhost',
]

INSTALLED_APPS = [
    'eventos',
    'usuarios',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'leaflet',
]

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


ROOT_URLCONF = 'vibeevents_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'vibeevents_core.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Araguaina'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', 
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (-10.18, -48.33),
    'DEFAULT_ZOOM': 13,
    'TILES': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'ATTRIBUTION_PREFIX': 'VibeEvents',
    'PLUGINS': {
        'geocoder': {
            'css': 'https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.css',
            'js': 'https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.js',
            'auto-include': True,
        }
    }
}

CSRF_TRUSTED_ORIGINS = [
    'https://halogen-delay-uncharted.ngrok-free.dev',
]

LOGIN_REDIRECT_URL = 'mapa_eventos'
LOGOUT_REDIRECT_URL = 'mapa_eventos'
LOGIN_URL = 'login' 
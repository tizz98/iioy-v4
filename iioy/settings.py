import environ
from celery.schedules import crontab

env = environ.Env(DEBUG=(bool, False),)  # set default values and casting
environ.Env.read_env()  # reading .env file

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='s&d2wyg@(p3jf1d&-1e!9az55_!j)_vbfu62_#x$=n5%4%27h8')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])


# Application definition

INSTALLED_APPS = [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party
    'django_extensions',
    'rest_framework',
    'corsheaders',

    # local
    'iioy.movies.apps.MoviesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'iioy.core.middleware.ZumhMiddleware',
]

ROOT_URLCONF = 'iioy.urls'
WSGI_APPLICATION = 'iioy.wsgi.application'
APPEND_SLASH = True


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': dict(
        env.db(),
        ATOMIC_REQUESTS=True,
    ),
}


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

if DEBUG:
    AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# External keys
TMDB_API_KEY = env('TMDB_API_KEY')
OMDB_API_KEY = env('OMDB_API_KEY')


# CORS
CORS_ORIGIN_WHITELIST = [
    'localhost:8080',
] + env.list('CORS_WHITELIST', default=[])

# DRF
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# Celery
CELERY_BROKER_URL = env('BROKER_URL')
CELERY_RESULT_BACKEND = env('RESULT_BACKEND')
CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERY_ALWAYS_EAGER = env.bool('ALWAYS_EAGER', default=False)
CELERY_BEAT_SCHEDULE = {
    'update_movie_lists': {
        'task': 'iioy.movies.tasks.update_movie_lists',
        'schedule': crontab(minute='0', hour='7', day_of_week=3),  # every wednesday, midnight PST
    },
    'update_genres': {
        'task': 'iioy.movies.tasks.update_genres',
        'schedule': crontab(minute='0', hour='7', day_of_week=1),  # every monday, midnight PST
    },
    'update_missing_movie_data': {
        'task': 'iioy.movies.tasks.update_missing_data_movies',
        'schedule': crontab(minute='0', hour='7', day_of_week=2),  # every tuesday, midnight PST
    },
    'update_missing_ratings': {
        'task': 'iioy.movies.tasks.update_missing_ratings',
        'schedule': crontab(minute='0', hour='7', day_of_week=0),  # every sunday, midnight PST
    },
}

from pathlib import Path
from decouple import Config, RepositoryEnv
from django.contrib.messages import constants as messages
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path('/data/web')

DOTENV_FILE_PATH = os.path.join(BASE_DIR, 'dotenv_files', '.env')

env_config = Config(RepositoryEnv(DOTENV_FILE_PATH))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_config('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = [
    h.strip() for h in env_config('ALLOWED_HOSTS', '').split(',')
    if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    url.strip() for url in env_config('CSRF_TRUSTED_ORIGINS', default='http://localhost:8080').split(',')
    if url.strip()
]


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THRID_PARTY_APPS = [
    'django_filters',
    'django_htmx',
    'django_summernote',
    'django_tomselect',
    'django_weasyprint',
]

LOCAL_APPS = [
    'core',
    'alternative',
    'discipline',
    'question',
    'user',
    'activity',
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THRID_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_tomselect.middleware.TomSelectMiddleware",
]

ROOT_URLCONF = 'core.urls'

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
                "django_tomselect.context_processors.tomselect",
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': env_config('DB_ENGINE'),
            'NAME': env_config('POSTGRES_DB'),
            'USER': env_config('POSTGRES_USER'),
            'PASSWORD': env_config('POSTGRES_PASSWORD'),
            'HOST': env_config('POSTGRES_HOST'),
            'PORT': env_config('POSTGRES_PORT')
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-Br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static',),
    os.path.join(BASE_DIR, 'node_modules'),
]

STATIC_ROOT = os.path.join(DATA_DIR, 'static')
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')

MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Bootstrap alerts configuration
MESSAGE_TAGS = {
    messages.SUCCESS: 'success',
    messages.ERROR: 'danger',
}

# Summernote configurations
SUMMERNOTE_THEME = 'bs4'

SUMMERNOTE_CONFIG = {
    'css': (
        '//cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css',
    ),

    'js': (
        '//cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js',
        '//cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js',
        '//cdn.jsdelivr.net/gh/tylerecouture/summernote-math@master/summernote-math.js',
    ),
    'lang': 'pt-BR',
    'summernote': {
        'placeholder': 'Digite o enunciado da questão...',
        'width': '100%',
        'height': '300px',
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline',
                      'strikethough', 'clear', 'superscript']],
            ['fontnames', ['fontname']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph', 'lineHeight','height']],
            ['table', ['table']],
            ['insert', ['picture', 'hr', 'math']],
            ['view', ['fullscreen', 'codeview', 'help', 'undo']],
        ]
    }
}

# Custom user configuration
AUTH_USER_MODEL = 'user.User'

# Login configuration
LOGIN_URL = 'user:login'

LOGIN_REDIRECT_URL = 'question:list'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env_config('EMAIL_HOST')
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env_config('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = env_config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env_config('DEFAULT_FROM_EMAIL')

# Password reset configuration
PASSWORD_RESET_TIMEOUT = 1800

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

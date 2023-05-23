"""
Please pay attention to the comments inside the code
"""


from pathlib import Path
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-!qqq@ykmqrm!wlb7u4xn2(_j+1#g^y&-sh$3ttztwqfz5x1(%8'
#for deploy please False the    DEBUG
DEBUG = True
#for deploy setup the allowed  host
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'users.apps.UsersConfig',
    'buildings.apps.BuildingsConfig',
    'otp.apps.OtpConfig',
    'announcements.apps.AnnouncementsConfig',
    'tickets.apps.TicketsConfig',
    'financials.apps.FinancialsConfig',
    'advertisements.apps.AdvertisementsConfig',
    'notifications.apps.NotificationsConfig',
    'poll.apps.PollConfig',
    'rest_framework_simplejwt',
    'rest_framework_swagger',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_email',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# rest_framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# Password validation




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


AUTH_USER_MODEL = "users.User"

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Regex
# https://www.datisnetwork.com/phone-number-regex.html
# must start with 09 and have 9 more digits
PHONE_REGEX = r"^09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}$"

# Minimum eight characters, at least one letter and one number
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,24}$"

# (username is 8-50 characters long), (no _ or . at the beginning),
# (no __ or _. or ._ or .. inside), (allowed characters), (no _ or . at the end)
USERNAME_REGEX = r"^(?=.{8,50}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"

# email --- this option is for setting email'
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = 'alizare0017@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'alizare0017@gmail.com'
EMAIL_HOST_PASSWORD = 'ufsthgehhlejoayu'



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'Project API',
    'DESCRIPTION': 'Building Manager',
    'VERSION': '1.0.0',
}


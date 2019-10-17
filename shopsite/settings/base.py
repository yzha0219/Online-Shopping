"""
Django settings for shopsite project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's1mivna_#&l99j$t#6s#$6a$66#w#7t)0+_avey%nvfrbml0x3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SET THE CART ID
CART_SESSION_ID = 'cart'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rosetta',
    'parler',
    'user.apps.UserConfig',
    'seller.apps.SellerConfig',
    'buyer.apps.BuyerConfig',
    'shop.apps.ShopConfig',
    'post.apps.PostConfig',
    'product.apps.ProductConfig',
    'order.apps.OrderConfig',
    'image.apps.ImageConfig',
    'comment.apps.CommentConfig',
    'cart.apps.CartConfig',
    'payment.apps.PaymentConfig',
    'activity.apps.ActivityConfig',
    'rest_framework',
    'snippets.apps.SnippetsConfig',
    'django.contrib.auth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shopsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shopsite.wsgi.application'

#Cookies Related Settings

#Cookies Expirations Time
COOKIE_EXPIRE_TIME = 3600 * 24
COOKIE_SALT_VALUE = 'shopsite'

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

# Redis Configurations
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', _('English')),
    ('zh-hans', _('Chinese')),
)

PARLER_LANGUAGES = {
    None: (
        {'code': 'en'},
        {'code': 'zh-hans'},
    ),
    'default': {
        'fallback': 'en',
        'hide_untranslated': False,
    }
}

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Rest Framework Settings for permissions and pagination
REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}
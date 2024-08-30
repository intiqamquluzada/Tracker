# production.py
from .base import Base
import os


class Production(Base):
    DEBUG = False
    ALLOWED_HOSTS = ['aasolutionsbackend.online']

    # DB configs
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': str(os.getenv('POSTGRES_DB')),
            'USER': str(os.getenv('POSTGRES_USER')),
            'PASSWORD': str(os.getenv('POSTGRES_PASSWORD')),
            'HOST': str(os.getenv('POSTGRES_HOST')),
            'PORT': '5432',
        }}

    # Secure settings for production
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_SSL_REDIRECT = True

    # CORS configs
    CORS_ALLOW_METHODS = [
        "DELETE",
        "GET",
        "OPTIONS",
        "PATCH",
        "POST",
        "PUT",
    ]

    CORS_ALLOW_ALL_ORIGINS = True
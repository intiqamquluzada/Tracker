

# base.py
import os

from configurations import Configuration
from pathlib import Path


class Base(Configuration):
    BASE_DIR = Path(__file__).resolve().parent.parent
    SECRET_KEY = "django-insecure-5c-x!4zyp=i!@&&_x-17rm4^z69_z9=s@m_@*h&i(w+r_+a%(4"
    DEBUG = False  # Default to False for security
    ALLOWED_HOSTS = []

    DJANGO_APPS = [
        'jazzmin',
        'modeltranslation',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

    LOCAL_APPS = [
        'apps.users.apps.UsersConfig',
    ]
    THIRD_PARTY_APPS = [
        'corsheaders',
    ]

    INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        "corsheaders.middleware.CorsMiddleware",
    ]

    ROOT_URLCONF = 'config.urls'

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
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'config.wsgi.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.getenv("REDIS_URL"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_TZ = True

    STATIC_URL = '/static/'

    if DEBUG:
        STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
    else:
        STATIC_ROOT = os.path.join(BASE_DIR, "static")

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



    LANGUAGES = (
        ("az", "az"),
        ("en", "en"),
        ("ru", "ru"),
    )

    LOCALE_PATHS = (
        os.path.join(BASE_DIR, 'locale'),
    )

    MODELTRANSLATION_DEFAULT_LANGUAGE = 'az'
    MODELTRANSLATION_LANGUAGES = ('az', 'en', 'ru')

    CKEDITOR_UPLOAD_PATH = "uploads/"

    CKEDITOR_CONFIGS = {
        'default': {
            'autoParagraph': False,
            'skin': 'moono',
            # 'skin': 'office2013',
            'allowedContent': True,
            'toolbar_Basic': [
                ['Source', '-', 'Bold', 'Italic']
            ],
            'toolbar_YourCustomToolbarConfig': [
                {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
                {'name': 'clipboard',
                 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
                {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
                {'name': 'forms',
                 'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                           'HiddenField']},
                '/',
                {'name': 'basicstyles',
                 'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
                {'name': 'paragraph',
                 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv',
                           'CreateSpan', '-',
                           'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                           'Language']},
                {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
                {'name': 'insert',
                 'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe',
                           'Span']},
                '/',
                {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
                {'name': 'colors', 'items': ['TextColor', 'BGColor']},
                {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
                {'name': 'about', 'items': ['About']},
                '/',  # put this to force next toolbar on new line
                {'name': 'yourcustomtools', 'items': [
                    # put the name of your editor.ui.addButton here
                    'Preview',
                    'Maximize',

                ]},
            ],
            'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
            # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
            # 'height': 291,
            # 'width': '100%',
            # 'filebrowserWindowHeight': 725,
            # 'filebrowserWindowWidth': 940,
            # 'toolbarCanCollapse': True,
            # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
            'tabSpaces': 4,
            'extraPlugins': ','.join([
                'uploadimage',  # the upload image feature
                # your extra plugins here
                'div',
                'autolink',
                'autoembed',
                'embedsemantic',
                'autogrow',
                # 'devtools',
                'widget',
                'lineutils',
                'clipboard',
                'dialog',
                'dialogui',
                'elementspath'
            ]),
        }
    }

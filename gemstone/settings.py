
from environ import Env
env = Env()
Env.read_env()
ENVIRONMENT = env('ENVIRONMENT', default='production')

if ENVIRONMENT == 'development':
    DEBUG = True
else:
    DEBUG = False

SECRET_KEY = env("SECRET_KEY")

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import dj_database_url


ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'category',
    'accounts',
    'store',
    'carts',
    "orders",

    'admin_honeypot',
    'crispy_forms',
    "crispy_bootstrap4",
    'phone_field',
    # 'ckeditor',
    # 'ckeditor_uploader',
    'notifications',
    'django_ckeditor_5',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'gemstone.urls'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

CRISPY_TEMPLATE_PACK = "bootstrap4"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.notification_count',
                "accounts.context_processors.unread_notifications",
                'category.context_processors.menu_categories',
                'carts.context_processors.counter',
                'accounts.context_processors.profile_picture',
            ],
        },
    },
]

WSGI_APPLICATION = 'gemstone.wsgi.application'

AUTH_USER_MODEL = 'accounts.Account'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    # 'mysql':{
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'azungdb',
    #     'USER': 'root',
    #     'PASSWORD': 'Hillarry',
    #     'HOST':'localhost',
    #     'PORT':'3306',
    # }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'azung_db',
#         'USER': 'postgres',
#         'PASSWORD': 'Hillarry',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
#



# POSTGRES_LOCALLY = False
# if ENVIRONMENT == 'production' or POSTGRES_LOCALLY == True:
#     DATABASES['default'] = dj_database_url.parse(env('DATABASE_URL'))

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),

]


MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
# if ENVIRONMENT == 'production' or POSTGRES_LOCALLY == True:
#     DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
# else:
#     MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')

# cloudinary storage
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUD_NAME'),
    'API_KEY': env('CLOUD_API_KEY'),
    'API_SECRET': env('CLOUD_API_SECRET'),
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger',

}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

CKEDITOR_UPLOAD_PATH = 'uploads/'
#
# CKEDITOR_CONFIGS = {
#     'default': {
#         'toolbar': 'full',
#         'height': 300,
#         'width': "100%",
#     },
# }

SESSION_REMEMBER_ME_EXPIRY = 2592000  # 30 days in seconds
TELEGRAM_BOT_TOKEN = "6919097745:AAG07P5y7uegerGTrQcA1u7GPT_9gzOicU8"
chat_id = '5102556482'


#ckeditor

customColorPalette = [
    {
        'color': 'hsl(4, 90%, 58%)',
        'label': 'Red'
    },
    {
        'color': 'hsl(340, 82%, 52%)',
        'label': 'Pink'
    },
    {
        'color': 'hsl(291, 64%, 42%)',
        'label': 'Purple'
    },
    {
        'color': 'hsl(262, 52%, 47%)',
        'label': 'Deep Purple'
    },
    {
        'color': 'hsl(231, 48%, 48%)',
        'label': 'Indigo'
    },
    {
        'color': 'hsl(207, 90%, 54%)',
        'label': 'Blue'
    },
]


CKEDITOR_5_CONFIGS = {
'default': {
    'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

},
"comment": {
    "language": {"ui": "en", "content": "en"},
    "toolbar": [
        "heading",
        "|",
        "bold",
        "italic",
        "link",
        "bulletedList",
        "numberedList",
        "blockQuote",
    ],
},
'extends': {
    'blockToolbar': [
        'paragraph', 'heading1', 'heading2', 'heading3',
        '|',
        'bulletedList', 'numberedList',
        '|',
        'blockQuote',
    ],
    'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'insertTable',
    'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                'strikethrough',],
    'image': {
        'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                    'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|', 'imageStyle:rounded', 'imageStyle:roundedSmall', 'imageStyle:roundedMedium', 'imageStyle:roundedLarge'],
        'styles': [
            'full',     'side', 'alignLeft','alignRight',  'alignCenter', 'rounded', 'roundedSmall', 'roundedMedium', 'roundedLarge'
        ]

    },
    'table': {
        'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
        'tableProperties', 'tableCellProperties' ],
        'tableProperties': {
            'borderColors': customColorPalette,
            'backgroundColors': customColorPalette
        },
        'tableCellProperties': {
            'borderColors': customColorPalette,
            'backgroundColors': customColorPalette
        }
    },
    'heading' : {
        'options': [
            { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
            { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
            { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
            { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
        ]
    }
},
'list': {
    'properties': {
        'styles': 'true',
        'startIndex': 'true',
        'reversed': 'true',
    }
}
}
CKEDITOR_5_USER_LANGUAGE=True
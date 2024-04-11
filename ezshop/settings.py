import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure-$^&k6)rkdqe$++!*^-(&kojpfpi*-%2#_f!1sf898rkb-ju^zq'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'mail.mitesolutions.com'  # Replace 'smtp.example.com' with your SMTP server
# EMAIL_PORT = 465  # Replace with the port of your SMTP server
# EMAIL_USE_TLS = True  # Set it to True if your SMTP server uses TLS
# EMAIL_HOST_USER = 'nasbeer@mitesolutions.com'  # Replace with your email address
# EMAIL_HOST_PASSWORD = 'MTqa@#748857'  # Replace with your email password

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mx.mailslurp.com'  # Replace 'smtp.example.com' with your SMTP server
EMAIL_PORT = 25  # Replace with the port of your SMTP server
EMAIL_USE_TSL = False  # Set it to True if your SMTP server uses TLS
EMAIL_HOST_USER = '3XuAF86a05YLhLwO2vYB3oykQflir7J1'  # Replace with your email address
EMAIL_HOST_PASSWORD = 'y05g7jL61VapbV2eFOrCqrd2FVNJeWrB'  # Replace with your email password

# EMPLOYEE_LOGIN_URL = 'employee_login'  # Define the URL for employee login

# # Set the LOGIN_URL for the Employee model
LOGIN_URL = '/login/'


DEBUG = True
USE_TZ = True
ALLOWED_HOSTS = ['ezshopapp.onrender.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'clearcache',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'ezshopapp',
    'corsheaders',
    "bootstrap_daterangepicker",

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    'ezshopapp.middleware.DisableClientSideCacheMiddleware',
    
]

CSRF_COOKIE_SECURE = True  # Ensure CSRF cookie is marked as secure for HTTPS
CSRF_COOKIE_HTTPONLY = True  # Ensure CSRF cookie is marked as HTTP-only
CSRF_COOKIE_SAMESITE = 'Strict'  # Ensure CSRF cookie is only sent with same-site requests
SESSION_COOKIE_AGE = 19800
SESSION_COOKIE_SECURE = True  # Ensure session cookie is marked as secure for HTTPS
SESSION_COOKIE_HTTPONLY = True  # Ensure session cookie is marked as HTTP-only


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:59917',
    # Add other allowed origins as needed
]



ROOT_URLCONF = 'ezshop.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'ezshop.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'ENGINE': 'django.db.backends.mysql',
        # 'OPTIONS': {
        #     'init_command': "SET sql_mode='STRICT_TRANS_TABLES",
        # },
        # 'USER': 'root',
        # 'PASSWORD': 'Mite@2024!',
        # 'HOST': 'localhost',
        # 'PORT': '3307',
        # 'NAME': 'ezshopdb',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'ezshopdb',  # Replace with your database name
#         'USER': 'root',  # Replace with your database username
#         'PASSWORD': 'El2m63fqXH9eQczR0HF98v4qtaM3PfDu',  # Replace with your database password
#         'HOST': 'dpg-co4q5ncf7o1s738vjdk0-a',  # Replace with your database host
#         'PORT': '5432',  # Replace with your database port
#     }
# }

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

TIME_ZONE = 'Asia/Dubai'

USE_I18N = True

USE_TZ = True

X_FRAME_OPTIONS = 'ALLOWALL'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/ezshopapp/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'ezshopapp/')

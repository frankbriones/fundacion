"""
Django settings for fund5 project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

# import os

# # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-v=q6ry5d8=bcpczvblq68xc(n*hg0#_9b4p65(tc162f#0nb*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['heroku.com', '127.0.0.1']

#https://pypi.org/project/django-admin-interface/
# Application definition
INSTALLED_APPS = [ 
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'comentario',
    #generar documentacion de django
    'django.contrib.admindocs',
    #'social.apps.django_app.default',
    #'django.contrib.gis',
    'rest_framework',
    'crispy_forms',
    'persona',
    'donacion',
    'talleres',
    'programa',
    'mathfilters',
    'bootstrap4',
    'website',
    'restapi',
    'rest_framework.authtoken',
    


]

#ACCOUNT_ACTIVATION_DAYS = 7


CRISPY_TEMPLATE_PACK = 'bootstrap4'


BOOTSTRAP4 = {
    'include_jquery': True,
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #middleware para el cambio de idioma a espanol mas el 
    #cambio en la internationalizacion
    'django.middleware.locale.LocaleMiddleware',
    'fund5.middleware.ProfileCompletoMiddleware',
]

ROOT_URLCONF = 'fund5.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [
            os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'fund5.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'FND5',
        'USER': 'name',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',      
    }
}




# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'es'


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'

# en produccion dirige al path de los estaticos
#STATIC_ROOT = '/Users/franklin/Desktop/Fund4/fund5/static/'


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)



STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

        

LOGIN_URL = '/modulo-usuario/login/'
LOGIN_REDIRECT_URL = '/modulo-usuario/perfil/'
LOGOUT_REDIRECT_URL = '/'




#envio de correo para recuperrar contrasena
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' # servicio de correo smtp
EMAIL_PORT = 587   #tambien se puede usar el puerto 25
EMAIL_HOST_USER = 'javier1992frank@gmail.com' # id de correo electrónico
EMAIL_HOST_PASSWORD = 'franklin1992' #password
EMAIL_USE_TLS = True


EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'correos_enviados')




#para el mapa que se encuentra en visitanos de  la website (API KEY)
#console.developers.google
#EASY_MAPS_GOOGLE_KEY = 'AIzaSyChphb-2I2kXUXmRB_0AIv272gZjbYUpfY'
#EASY_MAPS_CENTER = (-2.188168, -79.895279)

GOOGLE_MAPS_API_KEY = 'AIzaSyChphb-2I2kXUXmRB_0AIv272gZjbYUpfY'



#
AUTH_USER_MODEL = 'persona.Profile'


SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SESSION_COOKIE_AGE = 100  # para prueba solo ponemos 10 segundos para colocar 
                        #minutos solo colocamos la cantidad en segundos
SESSION_SAVE_EVERY_REQUEST = True



#GDAL_LIBRARY_PATH = 'C:/OSGeo4W64/bin/gdal202.dll/'




# REST_FRAMEWORK = {
#     # Use Django's standard `django.contrib.auth` permissions,
#     # or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': [
#         #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#         'rest_framework.permissions.IsAuthenticated'
#     ]
# }


db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
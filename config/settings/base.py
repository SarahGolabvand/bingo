from environ import Env
from pathlib import Path


# ENTRYPOINT

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ENVIRONMENTS
env = Env()

Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env('ALLOWED_HOSTS',default=['127.0.0.1', 'localhost'])



# INSTALLED_APPS = [
#     "django.contrib.contenttypes",
#     "django.contrib.auth",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
    

# ]
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware', 
    
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]


# DJANGO TENANTS DATABASE SETTINGS

PUBLIC_SCHEMA_URLCONF = 'config.urls-public'
ROOT_URLCONF = 'config.urls-tenants'


SHARED_APPS = (
    'django_tenants', 
    'apps.tenants',    

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "apps.frontend",
)

TENANT_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    
    # اپلیکیشن‌های بیزنس کافه (بعداً اضافه می‌کنیم):
    # 'apps.menus',
    # 'apps.tables',
    # 'apps.orders',
)

INSTALLED_APPS = list(SHARED_APPS) + [
    app for app in TENANT_APPS if app not in SHARED_APPS
]

TENANT_MODEL = "tenants.Client"
TENANT_DOMAIN_MODEL = "tenants.Domain"
PUBLIC_SCHEMA_NAME = 'public'

DATABASES = {
    'default': env.db('DATABASE_URL', engine='django_tenants.postgresql_backend')
}

DATABASES['default']['ENGINE'] = 'django_tenants.postgresql_backend'

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)
###########################################################
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

LANGUAGE_CODE = "en"
LANGUAGES = [("en", "English"), ("fa", "فارسی")]
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / "locale"]

STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR / "static"]

STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

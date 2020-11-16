import logging.config
import environ

print("Common config included")

logger = logging.getLogger("stockazio_api.config")
ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path("controllers")
BASE_DIR = environ.Path(__file__) - 3

env = environ.Env()

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# Logging
# ------------------------------------------------------------------------------
LOGLEVEL = env("LOGLEVEL", default="info").upper()
LOGGING_CONFIG = None
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"console": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"}},
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "console"},
            # # Add Handler for Sentry for `warning` and above
            # 'sentry': {
            #     'level': 'WARNING',
            #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            # },
        },
        "loggers": {
            "stockazio_api": {
                "level": LOGLEVEL,
                "handlers": ["console"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "": {"level": "WARNING", "handlers": ["console"]},
        },
    }
)

env_file = env("ENV_FILE", default=None)
if env_file:
    logger.info("Loading specified env file at %s", env_file)
    # we have an explicitely specified env file
    # so we try to load and it fail loudly if it does not exist
    env.read_env(env_file)
else:
    # we try to load from .env and config/.env
    # but do not crash if those files don't exist
    paths = [
        # /srv/stockazio/api/.env
        ROOT_DIR,
        # /srv/stockazio/.env
        (ROOT_DIR - 1),
    ]
    for path in paths:
        try:
            env_path = path.file(".env")
        except FileNotFoundError:
            logger.debug("No env file found at %s/.env", path)
            continue
        env.read_env(env_path)
        logger.info("Loaded env file at %s/.env", path)
        break

# CFG = hostname, protocol
STOCKAZIO_HOSTNAME = env("STOCKAZIO_HOSTNAME", default=None)
STOCKAZIO_PROTOCOL = env("STOCKAZIO_PROTOCOL", default="https")
STOCKAZIO_URL = env("STOCKAZIO_URL", default=f"{STOCKAZIO_PROTOCOL}://{STOCKAZIO_HOSTNAME}")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[]) + [STOCKAZIO_HOSTNAME]
INTERNAL_IPS = ALLOWED_HOSTS

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.admin",
]

THIRD_PARTY_APPS = [
    "mptt",
    "imagekit",
    "crispy_forms",
    "django_admin_listfilter_dropdown",
    "bootstrap4",
    "oauth2_provider",
    "corsheaders",
    "rest_framework",
    "django_extensions",
    "drf_yasg",
    "silk",
]

LOCAL_APPS = [
    "controllers.users",  # custom users app
    "controllers.app",
    "controllers.oauth",
    "controllers.part",
    "controllers.footprints",
    "controllers.storage",
    "controllers.categories",
    "controllers.manufacturer",
    "controllers.distributor",
    "controllers.OrdersImporter",
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps

ADDITIONAL_APPS = env.list("ADDITIONAL_APPS", default=[])
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + ADDITIONAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
ADDITIONAL_MIDDLEWARES_BEFORE = env.list("ADDITIONAL_MIDDLEWARES_BEFORE", default=[])

MIDDLEWARE = ADDITIONAL_MIDDLEWARES_BEFORE + [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "silk.middleware.SilkyMiddleware",
]

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------

# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="StockazIO <noreply@{}>".format(STOCKAZIO_HOSTNAME))

EMAIL_SUBJECT_PREFIX = env("EMAIL_SUBJECT_PREFIX", default="[StockazIO] ")
SERVER_EMAIL = env("SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)


EMAIL_CONFIG = env.email_url("EMAIL_CONFIG", default="consolemail://")

vars().update(EMAIL_CONFIG)

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    "default": env.db("DATABASE_URL")
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
# CONN_MAX_AGE seems to causes issues
# DATABASES["default"]["CONN_MAX_AGE"] = env("DB_CONN_MAX_AGE", default=60 * 5)

MIGRATION_MODULES = {
    # see https://github.com/jazzband/django-oauth-toolkit/issues/634
    # swappable models are badly designed in oauth2_provider
    # ignore migrations and provide our own models.
    "oauth2_provider": None,
}

#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db.sqlite3',
#     }
# }
# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "UTC"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "debug": DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "dealer.contrib.django.context_processor"
                # Your stuff: custom template context processors go here
            ],
        },
    }
]

# See: http://django-crispy-forms.readthedocs.org/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"
CRISPY_FAIL_SILENTLY = not DEBUG

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = env("STATIC_ROOT", default=str(ROOT_DIR("static")))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = env("STATIC_URL", default="/static/")

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = env("MEDIA_ROOT", default=str(APPS_DIR("media")))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = env("MEDIA_URL", default="/media/")
FILE_UPLOAD_PERMISSIONS = 0o644

ATTACHMENTS_UNATTACHED_PRUNE_DELAY = env.int("ATTACHMENTS_UNATTACHED_PRUNE_DELAY", default=3600 * 24)

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
SPA_URLCONF = "config.spa_urls"
ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = "config.wsgi.application"
ADMIN_URL = env("DJANGO_ADMIN_URL", default="^admin/")

# This ensures that Django will be able to detect a secure connection
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
LOGIN_URL = "/accounts/login"
LOGIN_REDIRECT_URL = "/parts"
LOGOUT_REDIRECT_URL = LOGIN_URL

AUTH_USER_MODEL = "users.User"

# AAA
PAGINATION = env(
    "PAGINATION",
    default={
        "DEFAULT": 25,
        "FOOTPRINTS": 5,
        "MANUFACTURERS": 10,
        "DISTRIBUTORS": 10,
        "STORAGES": 10,
        "PART_UNITS": 10,
        "PARAMETERS_UNITS": 10,
        "PARTS": 10,
        "ORDERS_IMPORTER": 10,
    },
)

# OAuth configuration
# ------------------------------------------------------------------------------
from controllers.oauth import scopes  # noqa

OAUTH2_PROVIDER = {
    "SCOPES": {s.id: s.label for s in scopes.SCOPES_BY_ID.values()},
    "ALLOWED_REDIRECT_URI_SCHEMES": ["http", "https", "urn"],
    # we keep expired tokens for 15 days, for tracability
    "REFRESH_TOKEN_EXPIRE_SECONDS": 3600 * 24 * 15,
    # 30 days
    "ACCESS_TOKEN_EXPIRE_SECONDS": 3600 * 24 * 30,
    "AUTHORIZATION_CODE_EXPIRE_SECONDS": 5 * 60,
    "OAUTH2_SERVER_CLASS": "controllers.oauth.server.OAuth2Server",
    "OAUTH2_BACKEND_CLASS": "controllers.oauth.backend.JsonAndHtml",
}
OAUTH2_PROVIDER_APPLICATION_MODEL = "oauth.Application"
OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL = "oauth.AccessToken"
OAUTH2_PROVIDER_GRANT_MODEL = "oauth.Grant"
OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL = "oauth.RefreshToken"


REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        # "rest_framework.authentication.BasicAuthentication",  # disable thoses or we will have
        # "rest_framework.authentication.SessionAuthentication",  # some annoying CSRF issues
    ),
    "DEFAULT_PERMISSION_CLASSES": ("controllers.oauth.permissions.ScopePermission",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "NUM_PROXIES": env.int("NUM_PROXIES", default=1),
}


# Various other things
PART_ATTACHMENT_ALLOWED_TYPES = env(
    "PART_ATTACHMENT_ALLOWED_TYPES",
    default=[
        "application/pdf",
        "application/xml",
        "image/gif",
        "image/jpeg",
        "image/png",
        "image/svg+xml",
        "text/html",
        "text/plain",
        "text/xml",
        "application/msword",
        "application/vnd.ms-excel",
        "application/vnd.oasis.opendocument.text",
        "application/vnd.oasis.opendocument.spreadsheet",
    ],
)

# https://github.com/jazzband/django-silk/issues/449
SILKY_INTERCEPT_FUNC = lambda r: DEBUG  # noqa: E731

# Mouser specific
MOUSER_API_KEY = env("MOUSER_API_KEY", default=None)
# Usuable values: None, All, Today, Yesterday, ThisWeek, LastWeek, ThisMonth, LastMonth, ThisQuarter, LastQuarter, ThisYear, LastYear or YearToDate
MOUSER_IMPORT_FILTER = env("MOUSER_IMPORT_FILTER", default="ThisMonth")

# 50M (50*1024*1024)
FILE_UPLOAD_MAX_MEMORY_SIZE = env("FILE_UPLOAD_MAX_MEMORY_SIZE", default=50 * 1024 * 1024)
DATA_UPLOAD_MAX_MEMORY_SIZE = FILE_UPLOAD_MAX_MEMORY_SIZE

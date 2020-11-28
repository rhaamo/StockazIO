# -*- coding: utf-8 -*-
"""
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .common import *  # noqa

print("DEBUG config included")

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", default=True)
FORCE_HTTPS_URLS = env.bool("FORCE_HTTPS_URLS", default=False)
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env("DJANGO_SECRET_KEY", default="^@*2wer5(q2k!f1)!bns&%gf_qliixb$cd)%k*=_blze$a4@%1")

# Mail settings
# ------------------------------------------------------------------------------
EMAIL_HOST = "localhost"
EMAIL_PORT = 25

# django-debug-toolbar
# ------------------------------------------------------------------------------

INTERNAL_IPS = ["127.0.0.1", "0.0.0.0", "192.168.10.167"]
ALLOWED_HOSTS = INTERNAL_IPS + ALLOWED_HOSTS

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
    # "SHOW_TOOLBAR_CALLBACK": lambda request: "debug" in request.GET,
    # "JQUERY_URL": "/staticfiles/admin/js/vendor/jquery/jquery.js",
}

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",  # slow down by 300ms
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",  # slow down by over9000 in admin
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    #    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]

# django-extensions
# ------------------------------------------------------------------------------
# INSTALLED_APPS += ('django_extensions', )

# Debug toolbar is slow, we disable it for tests
DEBUG_TOOLBAR_ENABLED = env.bool("DEBUG_TOOLBAR_ENABLED", default=DEBUG)
if DEBUG_TOOLBAR_ENABLED:
    MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)
    INSTALLED_APPS += ("debug_toolbar",)

ADDITIONAL_MIDDLEWARES_AFTER = ["silk.middleware.SilkyMiddleware"]

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# Your local stuff: Below this line define 3rd party library settings

CSRF_TRUSTED_ORIGINS = [o for o in ALLOWED_HOSTS]
CORS_ORIGIN_ALLOW_ALL = True

# Speed up a bit ImageKit
# if DEBUG=True, all caching is disabled, and calls to like /api/v1/footprints take ages...
IMAGEKIT_CACHE_BACKEND = "default"
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = "imagekit.cachefiles.strategies.Optimistic"
IMAGEKIT_DEFAULT_CACHEFILE_BACKEND = "imagekit.cachefiles.backends.Simple"

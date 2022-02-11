"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from django.urls import re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from controllers.utils import static

urlpatterns = [
    re_path(settings.ADMIN_URL, admin.site.urls),
    re_path(r"^oauth/", include(("controllers.oauth.urls", "oauth"), namespace="oauth")),
    re_path(r"^api/", include(("config.api_urls", "api"), namespace="api")),
]


admin.site.site_header = "StockazIO Inventory"
admin.site.site_title = "StockazIO Admin Portal"
admin.site.index_title = "Welcome to StockazIO"

if settings.DEBUG:
    # we don't really have choice, silk really wants to have them...
    urlpatterns += [re_path(r"^silk/", include("silk.urls", namespace="silk"))]

urlpatterns += static("/css/", document_root=settings.STOCKAZIO_SPA_CSS_ROOT)
urlpatterns += static("/js/", document_root=settings.STOCKAZIO_SPA_JS_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    print("Debug URLs enabled")
    import debug_toolbar

    urlpatterns = [re_path(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns
    urlpatterns += staticfiles_urlpatterns()

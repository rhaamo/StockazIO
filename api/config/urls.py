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
from django.conf.urls import static, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(settings.ADMIN_URL, admin.site.urls),
    url(r"^oauth/", include(("controllers.oauth.urls", "oauth"), namespace="oauth")),
    url(r"^api/", include(("config.api_urls", "api"), namespace="api")),
]


admin.site.site_header = "StockazIO Inventory"
admin.site.site_title = "StockazIO Admin Portal"
admin.site.index_title = "Welcome to StockazIO"

if settings.SILK_ENABLED:
    # we don't really have choice, silk really wants to have them...
    urlpatterns += [url(r"^silk/", include("silk.urls", namespace="silk"))]

urlpatterns += static.static("/css/", document_root=settings.STOCKAZIO_SPA_CSS_ROOT)
urlpatterns += static.static("/js/", document_root=settings.STOCKAZIO_SPA_JS_ROOT)

if settings.DEBUG:
    print("Debug URLs enabled")
    import debug_toolbar

    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns

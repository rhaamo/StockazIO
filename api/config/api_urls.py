from django.conf.urls import include, url
from rest_framework import routers

router = routers.DefaultRouter()
v1_patterns = router.urls

v1_patterns += [url(r"^app/", include(("controllers.app.urls", "app"), namespace="app"))]

urlpatterns = [url(r"v1/", include((v1_patterns, "v1"), namespace="v1"))]

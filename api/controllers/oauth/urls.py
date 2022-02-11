from django.conf.urls import re_path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"apps", views.ApplicationViewSet, "apps")
router.register(r"grants", views.GrantViewSet, "grants")

urlpatterns = router.urls + [
    re_path("^authorize/$", csrf_exempt(views.AuthorizeView.as_view()), name="authorize"),
    re_path("^token/$", views.TokenView.as_view(), name="token"),
    re_path("^revoke/$", views.RevokeTokenView.as_view(), name="revoke"),
    re_path("^check_token/$", views.CheckTokenview.as_view(), name="check_token"),
]

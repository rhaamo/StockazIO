from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^settings$", views.AppSettings.as_view(), name="settings"),
]

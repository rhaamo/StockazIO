from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r"^settings$", views.AppSettings.as_view(), name="settings"),
    re_path(r"^informations$", views.AppInformations.as_view(), name="informations"),
]

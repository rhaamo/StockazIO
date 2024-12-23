from django.urls import re_path
from rest_framework import routers

from controllers.OrdersImporter import views

router = routers.DefaultRouter()
router.register(r"category_matcher", views.CategoryMatcherViewSet, basename="CategoryMatcher")
router.register(r"", views.OrderViewSet, basename="OrdersImporter")

urlpatterns = [re_path(r"^lcsc_csv$", views.LcscCsvImporter.as_view(), name="LcscCsvImporter")]

urlpatterns = router.urls + urlpatterns

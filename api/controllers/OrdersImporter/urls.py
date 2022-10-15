from rest_framework import routers

from controllers.OrdersImporter import views

router = routers.DefaultRouter()
router.register(r"category_matcher", views.CategoryMatcherViewSet, basename="CategoryMatcher")
router.register(r"", views.OrderViewSet, basename="OrdersImporter")

urlpatterns = []

urlpatterns = router.urls + urlpatterns

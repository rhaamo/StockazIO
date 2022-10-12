from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"", views.CategoryViewSet, basename="Category")

urlpatterns = router.urls + []

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"categories", views.CategoryViewSet, basename="Category")

urlpatterns = router.urls + []

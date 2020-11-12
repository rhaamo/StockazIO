from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", views.ManufacturersViewSet, basename="Manufacturers")

urlpatterns = router.urls + []

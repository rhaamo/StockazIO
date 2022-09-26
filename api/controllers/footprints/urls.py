from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"tree", views.TreeViewSet, basename="FootprintsTree")
router.register(r"", views.FootprintViewSet, basename="Footprints")

urlpatterns = router.urls + []

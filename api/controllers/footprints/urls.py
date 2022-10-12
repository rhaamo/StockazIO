from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"tree", views.TreeViewSet, basename="FootprintsTree")

router.register(r"categories", views.FootprintCategoryViewSet, basename="FootprintCategories")

router.register(r"", views.FootprintViewSet, basename="Footprints")

urlpatterns = router.urls + []

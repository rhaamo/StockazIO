from django.conf.urls import include
from django.urls import re_path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = routers.DefaultRouter()
v1_patterns = router.urls

v1_patterns += [
    re_path(r"^app/", include(("controllers.app.urls", "app"), namespace="app")),
    re_path(r"^categories/", include(("controllers.categories.urls", "categories"), namespace="categories")),
    re_path(r"^footprints/", include(("controllers.footprints.urls", "footprints"), namespace="footprints")),
    re_path(r"^storages/", include(("controllers.storage.urls", "storage"), namespace="storages")),
    re_path(r"^parts/", include(("controllers.part.urls", "part"), namespace="parts")),
    re_path(r"^manufacturers/", include(("controllers.manufacturer.urls", "manufacturer"), namespace="manufacturers")),
    re_path(r"^distributors/", include(("controllers.distributor.urls", "distributor"), namespace="distributors")),
    re_path(
        r"^orders_importer/",
        include(("controllers.OrdersImporter.urls", "orders_importer"), namespace="orders_importer"),
    ),
    re_path(r"^projects/", include(("controllers.project.urls", "project"), namespace="projects")),
    re_path(
        r"^labeltemplates/", include(("controllers.labeltemplate.urls", "labeltemplate"), namespace="labeltemplates")
    ),
]

swagger = [
    re_path(r"^doc/schema$", SpectacularAPIView.as_view(), name="schema"),
    re_path(r"^doc/schema/swagger/", SpectacularSwaggerView.as_view(url_name="api:schema"), name="swagger"),
    re_path(r"^doc/schema/redoc/", SpectacularRedocView.as_view(url_name="api:schema"), name="redoc"),
]

urlpatterns = [re_path(r"v1/", include((v1_patterns, "v1"), namespace="v1"))] + swagger

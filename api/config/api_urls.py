from django.conf.urls import include
from django.urls import re_path
from rest_framework import routers
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

openapi_info = openapi.Info(
    title="StockazIO API",
    default_version="v1",
    description="StockazIO API",
    terms_of_service="https://github.com/rhaamo/stockazio",
    contact=openapi.Contact(email="stockazio@sigpipe.me"),
    license=openapi.License(name="Same as project"),
)

schema_view = get_schema_view(
    openapi_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

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
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns = [re_path(r"v1/", include((v1_patterns, "v1"), namespace="v1"))] + swagger

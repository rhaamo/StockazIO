from django.conf.urls import include, url
from rest_framework import routers
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="StockazIO API",
      default_version='v1',
      description="StockazIO API",
      terms_of_service="https://github.com/rhaamo/stockazio",
      contact=openapi.Contact(email="stockazio@sigpipe.me"),
      license=openapi.License(name="Same as project"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
v1_patterns = router.urls

v1_patterns += [
    url(r"^app/", include(("controllers.app.urls", "app"), namespace="app")),
    url(r"categories/", include(("controllers.categories.urls", "categories"), namespace="categories")),
    url(r"footprints/", include(("controllers.footprints.urls", "footprints"), namespace="footprints")),
    url(r"storages/", include(("controllers.storage.urls", "storage"), namespace="storages")),
    url(r"parts/", include(("controllers.part.urls", "part"), namespace="parts")),
    url(r"manufacturers/", include(("controllers.manufacturer.urls", "manufacturer"), namespace="manufacturers")),
    url(r"distributors/", include(("controllers.distributor.urls", "distributor"), namespace="distributors")),
]

swagger = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns = [url(r"v1/", include((v1_patterns, "v1"), namespace="v1"))] + swagger

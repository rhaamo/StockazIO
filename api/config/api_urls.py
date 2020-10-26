from django.conf.urls import include, url
from rest_framework import routers

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

urlpatterns = [url(r"v1/", include((v1_patterns, "v1"), namespace="v1"))]

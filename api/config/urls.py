"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls import static, url, include
import controllers.footprints.views as mbv_footprint
import controllers.storage.views as mbv_storage
import controllers.part.views.part_unit as mbv_part_unit
import controllers.part.views.parameters_unit as mbv_parameters_unit
import controllers.part.views.other as mbv_other
import controllers.part.views.part as mbv_part
import controllers.distributor.views as mbv_distributor
import controllers.manufacturer.views as mbv_manufacturer
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from controllers.part.views.common import CBVDeleteView, CBVDetailView
from django.urls import reverse_lazy
from controllers.footprints.models import FootprintCategory, Footprint
from controllers.storage.models import StorageCategory, StorageLocation
from controllers.part.models import PartUnit, ParametersUnit, Part
from controllers.manufacturer.models import Manufacturer
from controllers.distributor.models import Distributor
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(settings.ADMIN_URL, admin.site.urls),
    url(r"^oauth/", include(("controllers.oauth.urls", "oauth"), namespace="oauth")),
    url(r"^api/", include(("config.api_urls", "api"), namespace="api")),
    url(r"^$", RedirectView.as_view(pattern_name="part_list", permanent=True)),
    url(r"^accounts/login$", auth_views.LoginView.as_view(template_name="auth/login.html"), name="auth_login"),
    url(r"^accounts/logout$", auth_views.LogoutView.as_view(template_name="auth/logged_out.html"), name="auth_logout"),
    url(
        r"^password/reset$",
        auth_views.PasswordResetView.as_view(template_name="auth/password_reset_form.html"),
        name="password_reset",
    ),
    url(
        r"^password/reset/done$",
        auth_views.PasswordResetDoneView.as_view(template_name="auth/password_reset_done.html"),
        name="password_reset_done",
    ),
    url(
        r"^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$",
        auth_views.PasswordResetConfirmView.as_view(template_name="auth/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    url(
        r"^password/reset/complete$",
        auth_views.PasswordResetCompleteView.as_view(template_name="auth/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    url(
        r"^password/change$",
        auth_views.PasswordChangeView.as_view(template_name="auth/password_change.html"),
        name="password_change",
    ),
    url(
        r"^password/change/done$",
        auth_views.PasswordChangeDoneView.as_view(template_name="auth/password_change_done.html"),
        name="password_change_done",
    ),
    # Footprint Categories
    url(r"^footprints$", mbv_footprint.footprint_category_list, name="footprint_category_list"),
    url(r"^footprints/new$", mbv_footprint.footprint_category_create, name="footprint_category_create"),
    url(
        r"^footprints/(?P<pk>[0-9]+)/edit$",
        mbv_footprint.footprint_category_update,
        name="footprint_category_update",
    ),
    url(
        r"^footprints/(?P<pk>[0-9]+)/delete$",
        CBVDeleteView.as_view(
            model=FootprintCategory,
            success_url=reverse_lazy("footprint_category_list"),
            success_message="Footprint Category deleted successfully",
        ),
        name="footprint_category_delete",
    ),
    # Footprints
    url(r"^footprints/(?P<pk_category>[0-9]+)$", mbv_footprint.footprint_list, name="footprint_list"),
    url(r"^footprints/(?P<pk_category>[0-9]+)/sub_footprints$", mbv_footprint.footprint_list, name="footprint_list"),
    url(
        r"^footprints/(?P<pk_category>[0-9]+)/sub_footprints/new$",
        mbv_footprint.footprint_create,
        name="footprint_create",
    ),
    url(
        r"^footprints/(?P<pk_category>[0-9]+)/sub_footprints/(?P<pk>[0-9]+)/edit$",
        mbv_footprint.footprint_update,
        name="footprint_update",
    ),
    url(
        r"^footprints/(?P<pk_category>[0-9]+)/sub_footprints/(?P<pk>[0-9]+)/delete$",
        CBVDeleteView.as_view(
            model=Footprint,
            success_url=reverse_lazy("footprint_category_list"),
            success_message="Footprint deleted successfully",
        ),
        name="footprint_delete",
    ),
    # Distributors
    url(r"^distributors$", mbv_distributor.distributor_list, name="distributor_list"),
    url(
        r"^distributors/(?P<pk>[0-9]+)$",
        CBVDetailView.as_view(
            model=Distributor,
            template_name="distributors/distributor_detail.html",
        ),
        name="distributor_detail",
    ),
    url(r"^distributors/new$", mbv_distributor.distributor_create, name="distributor_create"),
    url(r"^distributors/(?P<pk>[0-9]+)/edit$", mbv_distributor.distributor_update, name="distributor_update"),
    url(
        r"^distributors/(?P<pk>[0-9]+)/delete$",
        CBVDeleteView.as_view(
            model=Distributor,
            success_url=reverse_lazy("distributor_list"),
            success_message="Distributor deleted successfully",
        ),
        name="distributor_delete",
    ),
    # Manufacturers
    url(r"^manufacturers$", mbv_manufacturer.manufacturer_list, name="manufacturer_list"),
    url(
        r"^manufacturers/(?P<pk>[0-9]+)$",
        CBVDetailView.as_view(
            model=Manufacturer,
            template_name="manufacturers/manufacturer_detail.html",
        ),
        name="manufacturer_detail",
    ),
    url(r"^manufacturers/new$", mbv_manufacturer.ManufacturerCreate.as_view(), name="manufacturer_create"),
    url(
        r"^manufacturers/(?P<pk>[0-9]+)/edit$",
        mbv_manufacturer.ManufacturerUpdate.as_view(),
        name="manufacturer_update",
    ),
    url(
        r"^manufacturers/(?P<pk>[0-9]+)/delete$",
        CBVDeleteView.as_view(
            model=Manufacturer,
            success_url=reverse_lazy("manufacturer_list"),
            success_message="Manufacturer deleted successfully",
        ),
        name="manufacturer_delete",
    ),
    # Storages Categories
    url(r"^storages$", mbv_storage.storage_category_list, name="storage_category_list"),
    url(r"^storages/tree$", mbv_storage.storage_tree, name="storage_tree"),
    url(r"^storages/new$", mbv_storage.storage_category_create, name="storage_category_create"),
    url(r"^storages/(?P<pk>[0-9]+)/edit$", mbv_storage.storage_category_update, name="storage_category_update"),
    url(
        r"^storages/(?P<pk>[0-9]+)/delete$",
        CBVDeleteView.as_view(
            model=StorageCategory,
            success_url=reverse_lazy("storage_category_list"),
            success_message="Storage Category deleted successfully",
        ),
        name="storage_category_delete",
    ),
    # Storages
    url(r"^storages/(?P<pk_category>[0-9]+)$", mbv_storage.storage_list, name="storage_list"),
    url(r"^storages/(?P<pk_category>[0-9]+)/sub_storages$", mbv_storage.storage_list, name="storage_list"),
    url(r"^storages/(?P<pk_category>[0-9]+)/sub_storages/new$", mbv_storage.storage_create, name="storage_create"),
    url(
        r"^storages/(?P<pk_category>[0-9]+)/sub_storages/(?P<pk>[0-9]+)/edit$",
        mbv_storage.storage_update,
        name="storage_update",
    ),
    url(
        r"^storages/(?P<pk_category>[0-9]+)/sub_storages/(?P<pk>[0-9]+)/delete$",
        CBVDeleteView.as_view(
            model=StorageLocation,
            success_url=reverse_lazy("storage_category_list"),
            template_name="storages/storage_delete.html",
            success_message="Storage deleted successfully",
        ),
        name="storage_delete",
    ),
    # Part Units
    url(r"^part_units$", mbv_part_unit.part_unit_list, name="part_unit_list"),
    url(r"^part_units/new$", mbv_part_unit.part_unit_create, name="part_unit_create"),
    url(r"^part_units/(?P<pk>[0-9]+)/edit$", mbv_part_unit.part_unit_update, name="part_unit_update"),
    url(
        r"^part_units/(?P<pk>[0-9]+)/delete$",
        CBVDeleteView.as_view(
            model=PartUnit,
            success_url=reverse_lazy("part_unit_list"),
            template_name="part_units/part_unit_delete.html",
            success_message="Part Unit deleted successfully",
        ),
        name="part_unit_delete",
    ),
    # Parameters Units
    url(r"^parameters_units$", mbv_parameters_unit.parameters_unit_list, name="parameters_unit_list"),
    url(r"^parameters_units/new$", mbv_parameters_unit.parameters_unit_create, name="parameters_unit_create"),
    url(
        r"^parameters_units/(?P<pk>[0-9]+)/edit$",
        mbv_parameters_unit.parameters_unit_update,
        name="parameters_unit_update",
    ),
    url(
        r"^parameters_units/(?P<pk>[0-9]+)/delete$",
        CBVDeleteView.as_view(
            model=ParametersUnit,
            success_url=reverse_lazy("parameters_unit_list"),
            success_message="Parameters Unit deleted successfully",
        ),
        name="parameters_unit_delete",
    ),
    # Other Views
    url(r"^views/infos$", mbv_other.other_informations, name="other_informations"),
    url(r"^views/soldable$", mbv_other.soldable, name="soldable"),
    url(r"^views/soldable/category/(?P<category>[0-9a-zA-Z]+)$", mbv_other.soldable, name="soldable"),
    url(r"^views/public$", mbv_other.public, name="public"),
    url(r"^views/public/category/(?P<category>[0-9a-zA-Z]+)$", mbv_other.public, name="public"),
    # Parts
    url(r"^parts$", mbv_part.part_list, name="part_list"),
    url(r"^parts/(?P<pk>[0-9]+)$", mbv_part.part_details, name="part_details"),
    url(r"^parts/(?P<pk>[0-9]+).json$", mbv_part.part_details_json, name="part_details_json"),
    url(r"^parts/new$", mbv_part.PartCreate.as_view(), name="part_create"),
    url(r"^parts/quick_add$", mbv_part.PartQuickAdd.as_view(), name="part_quick_add"),
    url(r"^parts/category/(?P<category>[0-9a-zA-Z]+)$", mbv_part.part_list, name="part_list"),
    url(r"^parts/(?P<pk>[0-9]+)/edit$", mbv_part.PartUpdate.as_view(), name="part_update"),
    url(
        r"^parts/(?P<pk>[0-9]+)/delete$",
        CBVDeleteView.as_view(
            model=Part, success_url=reverse_lazy("part_list"), success_message="Part deleted successfully"
        ),
        name="part_delete",
    ),
]


admin.site.site_header = "StockazIO Inventory"
admin.site.site_title = "StockazIO Admin Portal"
admin.site.index_title = "Welcome to StockazIO"

# we don't really have choice, silk really wants to have them...
urlpatterns += [url(r"^silk/", include("silk.urls", namespace="silk"))]

if settings.DEBUG:
    print("Debug URLs enabled")
    import debug_toolbar

    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns

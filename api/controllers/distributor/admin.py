from django.contrib import admin
from .models import Distributor
from config.admin import CommonAdmin


class DistributorAdmin(CommonAdmin):
    list_display = (
        "name",
        "address",
        "url",
        "email",
        "comment",
        "phone",
        "fax",
    )
    search_fields = ("name",)


admin.site.register(Distributor, DistributorAdmin)

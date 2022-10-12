from config.admin import CommonAdmin
from django.contrib import admin

from .models import Distributor


class DistributorAdmin(CommonAdmin):
    list_display = (
        "name",
        "address",
        "url",
        "datasheet_url",
        "email",
        "comment",
        "phone",
        "fax",
    )
    search_fields = ("name",)


admin.site.register(Distributor, DistributorAdmin)

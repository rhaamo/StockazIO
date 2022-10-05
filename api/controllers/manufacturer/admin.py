from django.contrib import admin
from controllers.manufacturer.models import Manufacturer, ManufacturerAlias
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from config.admin import CommonAdmin


class AliasesInLine(admin.TabularInline):
    model = ManufacturerAlias
    extra = 1
    autocomplete_fields = ["manufacturer"]

class ManufacturerAdmin(CommonAdmin):
    list_display = (
        "id",
        "get_logo",
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
    inlines = [AliasesInLine]

    def get_logo(self, obj):
        if obj.logo:
            return mark_safe(
                "<a href='{url_img}' target='_blank'><img src='{url_img}'/></a>".format(url_img=obj.logo_mini.url)
            )

    get_logo.short_description = _("Logo")


admin.site.register(Manufacturer, ManufacturerAdmin)

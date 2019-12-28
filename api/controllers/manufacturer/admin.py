from django.contrib import admin
from .models import Manufacturer, ManufacturerLogo
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from config.admin import CommonAdmin


class ManufacturerLogoInLine(admin.TabularInline):
    model = ManufacturerLogo
    extra = 1


class ManufacturerAdmin(CommonAdmin):
    list_display = (
        "get_logo",
        "name",
        "address",
        "url",
        "email",
        "comment",
        "phone",
        "fax",
    )
    search_fields = ("name",)
    inlines = [
        ManufacturerLogoInLine,
    ]

    def get_logo(self, obj):
        if obj.logos.count() >= 1:
            return mark_safe(
                "<a href='{url_img}' target='_blank'><img src='{url_img}'/></a>".format(
                    url_img=obj.logos.first().logo_mini.url
                )
            )

    get_logo.short_description = _("Logo")


admin.site.register(Manufacturer, ManufacturerAdmin)

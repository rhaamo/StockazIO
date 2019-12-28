from django.contrib import admin
from .models import StorageCategory, StorageLocation
from config.admin import CommonAdmin
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _


class StorageLocationAdmin(CommonAdmin):
    list_display = ("name", "category", "get_picture")
    search_fields = ("name",)
    inlines = []

    def get_picture(self, obj):
        if obj.picture:
            return mark_safe(
                "<a href='{url_img}' target='_blank'><img src='{url_img}' width='100px'/></a>".format(
                    url_img=obj.picture_small.url
                )
            )

    get_picture.short_description = _("Picture")


admin.site.register(StorageCategory)
admin.site.register(StorageLocation, StorageLocationAdmin)

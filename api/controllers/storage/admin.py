from config.admin import CommonAdmin
from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from controllers.storage.models import Storage


class StorageAdmin(CommonAdmin):
    list_display = ("name", "description", "get_picture")
    search_fields = ("name",)
    inlines = []

    def get_picture(self, obj):
        if obj.picture:
            return mark_safe(
                "<a href='{url_img}' target='_blank'><img src='{url_img}' width='100px'/></a>".format(
                    url_img=obj.picture_medium.url
                )
            )

    get_picture.short_description = _("Picture")


admin.site.register(Storage, StorageAdmin)

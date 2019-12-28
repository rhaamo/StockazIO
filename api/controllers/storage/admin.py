from django.contrib import admin
from .models import StorageCategory, StorageLocation
from config.admin import CommonAdmin
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from mptt.admin import MPTTModelAdmin
from mptt.admin import TreeRelatedFieldListFilter


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
    list_filter = [("category", TreeRelatedFieldListFilter)]


admin.site.register(StorageCategory, MPTTModelAdmin)
admin.site.register(StorageLocation, StorageLocationAdmin)

from django.contrib import admin
from .models import Footprint, FootprintCategory
from config.admin import CommonAdmin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _


class FootprintInLine(admin.TabularInline):
    model = Footprint
    extra = 1


class FootprintCategoryAdmin(CommonAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = [FootprintInLine]


class FootprintAdmin(CommonAdmin):
    list_display = ("name", "description", "get_picture")
    search_fields = ("name",)

    def get_picture(self, obj):
        if obj.picture:
            return mark_safe(
                "<a href='{url_img}' target='_blank'><img src='{url_img}' width='100px'/></a>".format(
                    url_img=obj.picture_small.url
                )
            )

    get_picture.short_description = _("Picture")
    list_filter = ("footprint",)


admin.site.register(FootprintCategory, FootprintCategoryAdmin)
admin.site.register(Footprint, FootprintAdmin)

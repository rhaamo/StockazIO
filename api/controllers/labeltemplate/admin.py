from config.admin import CommonAdmin
from django.contrib import admin

from .models import LabelTemplate


class LabelTemplateAdmin(CommonAdmin):
    list_display = ("name", "template", "width", "height")
    readonly_fields = ("base_pdf",)
    search_fields = ("name",)


admin.site.register(LabelTemplate, LabelTemplateAdmin)

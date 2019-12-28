from django.contrib import admin
from .models import Part, PartUnit
from config.admin import CommonAdmin


class PartUnitAdmin(CommonAdmin):
    list_display = ("name", "short_name", "description")
    search_fields = ("name",)


class PartAdmin(CommonAdmin):
    list_display = (
        "name",
        "description",
        "storage",
        "category",
        "stock_qty",
        "stock_qty_min",
        "footprint",
        "internal_part_number",
    )
    search_fields = ("name",)
    inlines = []


admin.site.register(PartUnit, PartUnitAdmin)
admin.site.register(Part, PartAdmin)

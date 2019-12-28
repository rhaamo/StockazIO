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
        "stock_qty_min",
        "stock_qty",
        "part_unit",
        # "category",
        # "storage",
        "footprint",
        "comment",
        "production_remarks",
        "status",
        "condition",
        "internal_part_number",
    )
    search_fields = ("name",)
    inlines = []


admin.site.register(PartUnit, PartUnitAdmin)
admin.site.register(Part, PartAdmin)

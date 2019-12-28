from django.contrib import admin
from .models import Part
from config.admin import CommonAdmin


class PartAdmin(CommonAdmin):
    list_display = (
        "name",
        "description",
        "stock_qty_min",
        "stock_qty",
        # "part_unit",
        # "category",
        # "storage",
        # "footprint",
        "comment",
        "production_remarks",
        "status",
        "condition",
        "internal_part_number",
    )
    search_fields = ("name",)
    inlines = []


admin.site.register(Part, PartAdmin)

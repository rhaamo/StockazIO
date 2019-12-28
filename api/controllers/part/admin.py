from django.contrib import admin
from .models import Part, PartUnit, PartParameter, ParametersUnit
from config.admin import CommonAdmin
from controllers.distributor.models import DistributorSku
from controllers.manufacturer.models import PartManufacturer


class PartUnitAdmin(CommonAdmin):
    list_display = ("name", "short_name", "description")
    search_fields = ("name",)


class ParametersUnitAdmin(CommonAdmin):
    list_display = (
        "name",
        "prefix",
        "symbol",
        "description",
    )
    search_fields = ("name",)


class DistributorSkuInLine(admin.TabularInline):
    model = DistributorSku
    extra = 1


class PartManufacturerInLine(admin.TabularInline):
    model = PartManufacturer
    extra = 1


class PartParameterInLine(admin.TabularInline):
    model = PartParameter
    extra = 1


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
    inlines = [DistributorSkuInLine, PartManufacturerInLine, PartParameterInLine]


admin.site.register(PartUnit, PartUnitAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(ParametersUnit, ParametersUnitAdmin)

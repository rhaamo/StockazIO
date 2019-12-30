from django.contrib import admin
from .models import Part, PartUnit, PartParameter, ParametersUnit, PartAttachment
from config.admin import CommonAdmin
from controllers.distributor.models import DistributorSku
from controllers.manufacturer.models import PartManufacturer
from django_admin_listfilter_dropdown.filters import DropdownFilter
from mptt.admin import TreeRelatedFieldListFilter


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
    list_filter = ("name",)


class DistributorSkuInLine(admin.TabularInline):
    model = DistributorSku
    extra = 1
    autocomplete_fields = ["distributor"]


class PartManufacturerInLine(admin.TabularInline):
    model = PartManufacturer
    extra = 1
    autocomplete_fields = ["manufacturer"]


class PartParameterInLine(admin.TabularInline):
    model = PartParameter
    extra = 1
    autocomplete_fields = ["unit"]


class PartAttachmentInLine(admin.TabularInline):
    model = PartAttachment
    extra = 1


class PartAdmin(CommonAdmin):
    list_display = (
        "name",
        "description",
        "storage",
        # "category",
        "stock_qty",
        "stock_qty_min",
        "part_unit",
        "footprint",
        "internal_part_number",
    )
    search_fields = ["name"]
    inlines = [DistributorSkuInLine, PartManufacturerInLine, PartParameterInLine, PartAttachmentInLine]
    list_filter = [
        ("footprint__name", DropdownFilter),
        ("storage__name", DropdownFilter),
        ("category", TreeRelatedFieldListFilter),
    ]
    autocomplete_fields = ("storage", "category", "footprint")


class PartAttachmentAdmin(CommonAdmin):
    list_display = ("description",)


admin.site.register(PartUnit, PartUnitAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(ParametersUnit, ParametersUnitAdmin)
admin.site.register(PartAttachment, PartAttachmentAdmin)

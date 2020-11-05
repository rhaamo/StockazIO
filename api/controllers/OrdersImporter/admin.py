from django.contrib import admin
from config.admin import CommonAdmin
from .models import Order, Item, CategoryMatcher


class ItemInLine(admin.TabularInline):
    model = Item
    extra = 1
    # autocomplete_fields = [""]


class OrderAdmin(CommonAdmin):
    list_display = ("date", "order_number", "status", "vendor", "import_state")
    search_fields = ("order_number",)
    list_filter = (
        "status",
        "import_state",
        "vendor",
    )
    inlines = [ItemInLine]


class ItemAdmin(CommonAdmin):
    list_display = (
        "vendor_part_number",
        "mfr_part_number",
        "manufacturer",
        "description",
        "quantity",
        "order",
        "ignore",
    )
    search_fields = ("vendor_part_number", "mfr_part_number", "description")
    list_filter = ("manufacturer", "order")
    autocomplete_fields = ("category",)


class CategoryMatcherAdmin(CommonAdmin):
    list_display = ("regexp",)
    autocomplete_fields = ("category",)


admin.site.register(Order, OrderAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(CategoryMatcher, CategoryMatcherAdmin)

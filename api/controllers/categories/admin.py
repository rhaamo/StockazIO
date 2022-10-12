from config.admin import CommonAdmin
from django.contrib import admin

from controllers.categories.models import Category


class CategoryAdmin(CommonAdmin):
    list_display = ("id", "name", "parent")
    search_fields = ["name"]


admin.site.register(Category, CategoryAdmin)

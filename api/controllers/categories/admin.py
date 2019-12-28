from django.contrib import admin
from .models import Category
from config.admin import CommonAdmin


class CategoryAdmin(CommonAdmin):
    search_fields = ["name"]


admin.site.register(Category, CategoryAdmin)

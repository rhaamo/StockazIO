from django.contrib import admin
from .models import Category
from config.admin import CommonAdmin
from mptt.admin import MPTTModelAdmin


class CategoryAdmin(MPTTModelAdmin, CommonAdmin):
    search_fields = ["name"]


admin.site.register(Category, CategoryAdmin)

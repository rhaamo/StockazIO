from config.admin import CommonAdmin
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Category


class CategoryAdmin(MPTTModelAdmin, CommonAdmin):
    search_fields = ["name"]


admin.site.register(Category, CategoryAdmin)

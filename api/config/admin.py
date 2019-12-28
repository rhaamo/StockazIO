from django.contrib import admin


class CommonAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_select_related = True

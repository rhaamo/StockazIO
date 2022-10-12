from config.admin import CommonAdmin
from django.contrib import admin

from .models import Project, ProjectAttachment, ProjectPart


class ProjectAttachmentInLine(admin.TabularInline):
    model = ProjectAttachment
    extra = 1


class ProjectPartInLine(admin.TabularInline):
    model = ProjectPart
    extra = 1
    autocomplete_fields = ("part",)


class ProjectAdmin(CommonAdmin):
    list_display = ("id", "name", "description", "public", "created_at")
    search_fields = (
        "name",
        "description",
        "notes",
    )
    inlines = [ProjectAttachmentInLine, ProjectPartInLine]


class ProjectAttachmentAdmin(CommonAdmin):
    list_display = ("description",)


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectAttachment, ProjectAttachmentAdmin)

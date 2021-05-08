from django.db import models

from controllers.part.models import Part
from controllers.part.validators import validate_file_type


class Project(models.Model):
    STATES = ((1, "Planned"), (2, "Ongoing"), (3, "Finished"), (4, "On-hold"), (5, "Abandonned"), (99, "Unknown"))
    name = models.CharField("name", max_length=255, unique=False, blank=False)
    description = models.TextField("description", blank=True)
    notes = models.TextField("notes", blank=True)
    ibom_url = models.URLField("ibom url", blank=True)
    state = models.IntegerField("state", default=99, choices=STATES)
    public = models.BooleanField("public", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class ProjectPart(models.Model):
    project = models.ForeignKey(
        Project, related_name="project_parts", blank=False, null=False, on_delete=models.CASCADE
    )
    part = models.ForeignKey(Part, blank=True, null=True, on_delete=models.SET_NULL)
    part_name = models.CharField("part name", max_length=255, blank=True)
    qty = models.IntegerField("part quantity", default=1)
    sourced = models.BooleanField("sourced", default=False)
    notes = models.CharField("notes", max_length=255, blank=True)

    def __str__(self):
        if self.part:
            return self.part.name
        return self.part_name


class ProjectAttachment(models.Model):
    description = models.CharField(
        "description", max_length=100, blank=False, unique=False, help_text="Description of the attachment"
    )
    file = models.FileField(
        verbose_name="File",
        help_text="File to upload",
        upload_to="part_attachments/",
        validators=[validate_file_type],
        blank=False,
        null=False,
    )
    project = models.ForeignKey(
        Project, related_name="project_attachments", blank=False, null=False, on_delete=models.CASCADE
    )

    class Meta(object):
        ordering = ("id",)
        verbose_name = "Project Attachment"
        verbose_name_plural = "Project Attachments"

    def __str__(self):
        return self.description

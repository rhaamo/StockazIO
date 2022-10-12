import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from tree_queries.models import TreeNode


class Storage(TreeNode):
    name = models.CharField(max_length=200)
    description = models.CharField(_("description"), max_length=255, unique=False, blank=True)

    picture = models.ImageField(
        upload_to="storage_locations/",
        verbose_name=_("Storage location pictures"),
        blank=True,
        null=True,
        help_text=_("Storage location"),
    )
    picture_medium = ImageSpecField(
        source="picture", processors=[ResizeToFill(400, 400, upscale=False)], format="JPEG", options={"quality": 80}
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta(object):
        ordering = ("name",)
        verbose_name = _("storage location")
        verbose_name_plural = _("storage locations")

    def __str__(self):
        return self.name

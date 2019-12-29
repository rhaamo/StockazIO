from django.db import models
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from mptt.models import MPTTModel, TreeForeignKey


class StorageCategory(MPTTModel):
    name = models.CharField(max_length=200)
    parent = TreeForeignKey("self", blank=True, null=True, related_name="children", on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name_plural = _("storage categories")

    def __str__(self):
        return self.name


class StorageLocation(models.Model):
    name = models.CharField(_("name"), max_length=255, unique=False, blank=False)
    category = models.ForeignKey(StorageCategory, blank=True, null=True, on_delete=models.CASCADE)

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

    class Meta(object):
        ordering = ("name",)
        verbose_name = _("storage location")
        verbose_name_plural = _("storage locations")

    def __str__(self):
        return self.name

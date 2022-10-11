from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from mptt.models import MPTTModel, TreeForeignKey
import uuid
from mptt.templatetags.mptt_tags import tree_path
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


class StorageCategory(MPTTModel):
    name = models.CharField(max_length=200)
    parent = TreeForeignKey("self", blank=True, null=True, related_name="children", on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    
    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name_plural = _("storage categories")

    def __str__(self):
        return self.name


class StorageLocation(models.Model):
    name = models.CharField(_("name"), max_length=255, unique=False, blank=False)
    category = models.ForeignKey(
        StorageCategory, related_name="storage_locations", blank=False, null=False, on_delete=models.CASCADE
    )
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
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta(object):
        ordering = ("name",)
        verbose_name = _("storage location")
        verbose_name_plural = _("storage locations")

    def __str__(self):
        return self.name

    def get_category_path(self, separator=" > "):
        path = tree_path(self.category.get_ancestors(separator))
        if not path:
            return separator.join([self.category.name, self.name])
        return separator.join([path, self.category.name, self.name])

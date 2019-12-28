from django.db import models
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit


class FootprintCategory(models.Model):
    name = models.CharField(_("name"), max_length=255, unique=True, blank=False, help_text=_("ex. PDIP"))
    description = models.CharField(_("description"), max_length=255, unique=False, blank=True)

    class Meta(object):
        ordering = ("name",)
        verbose_name = _("footprint category")
        verbose_name_plural = _("footprint categories")

    def __str__(self):
        return self.name


class Footprint(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True, blank=False, help_text=_("ex. PBGA-260"))
    description = models.CharField(_("description"), max_length=255, unique=False, blank=True)
    picture = models.ImageField(
        upload_to="footprints/",
        verbose_name=_("Footprint picture"),
        blank=True,
        null=True,
        help_text=_("Footprint schematic"),
    )
    picture_mini = ImageSpecField(
        source="picture", processors=[ResizeToFit(50, 50, upscale=False)], format="JPEG", options={"quality": 80}
    )
    picture_small = ImageSpecField(
        source="picture", processors=[ResizeToFill(200, 150, upscale=False)], format="JPEG", options={"quality": 80}
    )
    picture_medium = ImageSpecField(
        source="picture", processors=[ResizeToFill(400, 400, upscale=False)], format="JPEG", options={"quality": 80}
    )

    footprint = models.ForeignKey(
        FootprintCategory,
        on_delete=models.CASCADE,
        verbose_name=_("Footprint"),
        help_text=_("Main category of the footprint"),
    )

    class Meta(object):
        ordering = ("name",)
        verbose_name = _("footprint")
        verbose_name_plural = _("footprints")

    def __str__(self):
        return self.name

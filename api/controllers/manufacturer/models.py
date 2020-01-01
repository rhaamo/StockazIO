from django.db import models
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from controllers.part.models import Part


class Manufacturer(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=False, unique=True, help_text=_("Name"))
    address = models.CharField(_("address"), max_length=255, blank=True, unique=False, help_text=_("Address"))
    url = models.CharField(_("url"), max_length=255, blank=True, unique=False, help_text=_("URL"))
    email = models.CharField(_("email"), max_length=255, blank=True, unique=False, help_text=_("Email"))
    comment = models.CharField(_("comment"), max_length=255, blank=True, unique=False, help_text=_("Comment"))
    phone = models.CharField(_("phone"), max_length=255, blank=True, unique=False, help_text=_("Phone"))
    fax = models.CharField(_("fax"), max_length=255, blank=True, unique=False, help_text=_("FAX"))

    class Meta(object):
        ordering = ("name",)
        verbose_name = _("Manufacturer")
        verbose_name_plural = _("Manufacturers")

    def __str__(self):
        return self.name


class ManufacturerLogo(models.Model):
    manufacturer = models.ForeignKey(
        Manufacturer, related_name="logos", blank=False, null=False, on_delete=models.PROTECT
    )

    logo = models.ImageField(upload_to="manufacturers/", verbose_name=_("Manufacturer logo"), blank=False, null=False)
    logo_mini = ImageSpecField(
        source="logo", processors=[ResizeToFit(50, 50, upscale=False)], format="JPEG", options={"quality": 80}
    )
    logo_small = ImageSpecField(
        source="logo", processors=[ResizeToFill(200, 150, upscale=False)], format="JPEG", options={"quality": 80}
    )
    logo_medium = ImageSpecField(
        source="logo", processors=[ResizeToFill(400, 400, upscale=False)], format="JPEG", options={"quality": 80}
    )

    class Meta(object):
        ordering = ("id",)
        verbose_name = _("Manufacturer Logo")
        verbose_name_plural = _("Manufacturer Logos")


class PartManufacturer(models.Model):
    sku = models.CharField(_("sku id"), max_length=255, blank=False, null=False)

    part = models.ForeignKey(Part, related_name="manufacturers_sku", blank=True, null=True, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(
        Manufacturer, related_name="parts_manufacturers_sku", blank=True, null=True, on_delete=models.PROTECT
    )

    class Meta(object):
        ordering = ("sku",)
        verbose_name = _("Part Manufacturer")
        verbose_name_plural = _("Part Manufacturers")

    def __str__(self):
        return self.sku

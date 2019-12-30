from django.db import models
from django.utils.translation import ugettext_lazy as _
from controllers.footprints.models import Footprint
from controllers.categories.models import Category
from controllers.storage.models import StorageLocation
from controllers.part.validators import validate_file_type


class PartUnit(models.Model):
    name = models.CharField(_("name"), max_length=255, unique=True, blank=False, help_text=_("ex. Centimeters"))
    short_name = models.CharField(_("short name"), max_length=255, unique=False, blank=False, help_text=_("ex. cms"))
    description = models.CharField(_("description"), max_length=255, unique=False, blank=True)

    class Meta(object):
        ordering = ("name",)
        verbose_name = _("part unit")
        verbose_name_plural = _("part units")

    def __str__(self):
        return "{0} ({1})".format(self.name, self.short_name)


class Part(models.Model):
    name = models.CharField(_("name"), max_length=255, unique=False, blank=False)
    description = models.CharField(
        _("description"),
        max_length=255,
        unique=False,
        blank=True,
        help_text=_("Description about the part functionalities"),
    )
    stock_qty_min = models.IntegerField(
        _("minimum stock quantity"),
        default=0,
        unique=False,
        blank=False,
        help_text=_("How many do you needs to have at minimum ?"),
    )
    stock_qty = models.IntegerField(
        _("stock quantity"), default=1, unique=False, blank=False, help_text=_("How many do you have now ?")
    )
    part_unit = models.ForeignKey(PartUnit, blank=True, null=True, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.PROTECT)
    storage = models.ForeignKey(StorageLocation, blank=True, null=True, on_delete=models.PROTECT)
    footprint = models.ForeignKey(Footprint, blank=True, null=True, on_delete=models.PROTECT)
    comment = models.CharField(
        _("comment"), max_length=255, unique=False, blank=True, help_text=_("Comments about the part itself")
    )
    production_remarks = models.CharField(
        _("production remarks"), max_length=255, unique=False, blank=True, help_text=_("Production remarks")
    )
    status = models.CharField(
        _("status"), max_length=255, unique=False, blank=True, help_text=_("Notes about the inventory sheet status ?")
    )
    needs_review = models.BooleanField(
        _("needs review"), default=False, unique=False, blank=False, help_text=_("Does this part notice needs review ?")
    )
    condition = models.CharField(
        _("condition"), max_length=255, unique=False, blank=True, help_text=_("Notes about some parts conditions ?")
    )
    can_be_sold = models.BooleanField(
        _("can be sold"), default=False, unique=False, blank=False, help_text=_("Are you willing to sold some parts ?")
    )
    private = models.BooleanField(
        _("private"), default=False, unique=False, blank=False, help_text=_("Oh no it's a private part !")
    )
    internal_part_number = models.CharField(
        _("internal part number"), max_length=255, unique=False, blank=True, help_text=_("Internal part number")
    )

    # Search vector

    class Meta(object):
        ordering = ("name",)
        verbose_name = _("part")
        verbose_name_plural = _("parts")

    def __str__(self):
        return self.name


class ParametersUnit(models.Model):
    name = models.CharField(_("name"), max_length=255, unique=False, blank=False, help_text=_("ex. Ampere"))
    symbol = models.CharField(_("symbol"), max_length=255, unique=False, blank=True, help_text=_("ex. A"))
    prefix = models.CharField(_("prefix"), max_length=255, unique=False, blank=True, help_text=_("ex. μ"))

    description = models.CharField(_("description"), max_length=255, unique=False, blank=True)

    # REL: parameters

    class Meta(object):
        ordering = ("name",)
        verbose_name = _("parameter unit")
        verbose_name_plural = _("parameter units")

    def __str__(self):
        if self.prefix or self.symbol:
            return "{0} ({1}{2})".format(self.name, self.prefix, self.symbol)
        else:
            return self.name


class PartParameter(models.Model):
    name = models.CharField(_("name"), max_length=255, unique=False, blank=False)
    description = models.CharField(_("description"), max_length=255, unique=False, blank=True)
    value = models.CharField(_("value"), max_length=255, unique=False, blank=False)
    unit = models.ForeignKey(ParametersUnit, blank=True, null=True, on_delete=models.PROTECT)

    part = models.ForeignKey(
        Part, related_name="part_parameters_value", blank=False, null=False, on_delete=models.CASCADE
    )

    class Meta(object):
        ordering = ("name",)
        verbose_name = _("Part parameter")
        verbose_name_plural = _("Part parameters")

    def __str__(self):
        return self.name


class PartAttachment(models.Model):
    description = models.CharField(
        _("description"), max_length=100, blank=False, unique=True, help_text=_("Description of the attachment")
    )
    file = models.FileField(
        verbose_name=_("File"),
        help_text=_("File to upload"),
        upload_to="part_attachments/",
        validators=[validate_file_type],
        blank=False,
        null=False,
    )
    part = models.ForeignKey(Part, related_name="part_attachments", blank=True, null=True, on_delete=models.CASCADE)

    class Meta(object):
        ordering = ("id",)
        verbose_name = _("Part Attachment")
        verbose_name_plural = _("Part Attachments")

    def __str__(self):
        return self.description

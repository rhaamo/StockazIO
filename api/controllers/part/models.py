from django.db import models
from django.utils.translation import ugettext_lazy as _


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
    # part_unit = models.ForeignKey(PartUnit, blank=True, null=True, on_delete=models.PROTECT)
    # category
    # storage location
    # footprint = models.ForeignKey(Footprint, blank=True, null=True, on_delete=models.PROTECT)
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

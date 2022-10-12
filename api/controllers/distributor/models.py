from django.db import models
from django.utils.translation import gettext_lazy as _

from controllers.part.models import Part

"""
Notes about datasheet_url, {placeholders} handled:
_ do nothing
sku sku as is
sku_lower sku in lowercase
sku_upper sku in uppercase
"""


class Distributor(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=False, unique=True, help_text=_("Name"))
    address = models.TextField(_("address"), blank=True, unique=False, help_text=_("Address"))
    url = models.CharField(_("url"), max_length=255, blank=True, unique=False, help_text=_("URL"))
    email = models.CharField(_("email"), max_length=255, blank=True, unique=False, help_text=_("Email"))
    comment = models.TextField(_("comment"), blank=True, unique=False, help_text=_("Comment"))
    phone = models.CharField(_("phone"), max_length=255, blank=True, unique=False, help_text=_("Phone"))
    fax = models.CharField(_("fax"), max_length=255, blank=True, unique=False, help_text=_("FAX"))
    datasheet_url = models.URLField("Datasheet URL", max_length=255, blank=True, unique=False)

    class Meta(object):
        ordering = ("name",)
        verbose_name = _("distributor")
        verbose_name_plural = _("distributors")

    def __str__(self):
        return self.name


class DistributorSku(models.Model):
    sku = models.CharField(_("sku id"), max_length=255, blank=False, null=False)

    part = models.ForeignKey(Part, related_name="distributors_sku", blank=True, null=True, on_delete=models.CASCADE)
    distributor = models.ForeignKey(
        Distributor, related_name="parts_distributors_sku", blank=False, null=False, on_delete=models.CASCADE
    )
    datasheet_url = models.URLField("Datasheet URL", max_length=255, blank=True, unique=False)

    class Meta(object):
        ordering = ("sku",)
        verbose_name = _("Distributor")
        verbose_name_plural = _("Distributors")

    def __str__(self):
        return self.sku

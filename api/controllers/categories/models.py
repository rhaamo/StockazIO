from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from mptt.templatetags.mptt_tags import tree_path


class Category(MPTTModel):
    name = models.CharField(max_length=200)
    parent = TreeForeignKey(
        "self", blank=True, null=True, related_name="children", on_delete=models.CASCADE, db_index=True
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    def get_category_path(self, separator=" > "):
        path = tree_path(self.parent.get_ancestors(separator))
        if not path:
            return self.parent.name
        return separator.join([path, self.parent.name])

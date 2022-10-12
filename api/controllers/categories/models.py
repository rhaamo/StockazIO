from django.db import models
from django.utils.translation import gettext_lazy as _
from tree_queries.models import TreeNode


class Category(TreeNode):
    name = models.CharField(max_length=200)

    class Meta(object):
        ordering = ["name"]
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

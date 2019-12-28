from django.db import models
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children", on_delete=models.CASCADE)

    class Meta:
        # enforcing that there can not be two categories under a parent with same slug
        # __str__ method elaborated later in post.  use __unicode__ in place of
        # __str__ if you are using python 2
        verbose_name_plural = _("categories")

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return " -> ".join(full_path[::-1])

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

PERMISSIONS_CONFIGURATION = {
    "categories": {"label": "Categories", "help_text": "", "scopes": {"read", "write"}},
    "parts": {"label": "Categories", "help_text": "", "scopes": {"read", "write"}},
}

PERMISSIONS = sorted(PERMISSIONS_CONFIGURATION.keys())

default_permissions = ["categories", "parts"]


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=False)

    class Meta:
        db_table = "auth_user"

    def get_permissions(self, defaults=[]):
        perms = {}
        for p in PERMISSIONS:
            v = (
                self.is_superuser
                or p in defaults
            )
            perms[p] = v
        return perms

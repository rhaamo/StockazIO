from django.contrib.auth.models import AbstractUser

PERMISSIONS_CONFIGURATION = {
    "categories": {"label": "Categories", "help_text": "", "scopes": {"read", "write"}},
    "parts": {"label": "Categories", "help_text": "", "scopes": {"read", "write"}},
}

PERMISSIONS = sorted(PERMISSIONS_CONFIGURATION.keys())

default_permissions = ["categories", "parts"]


class User(AbstractUser):
    class Meta:
        db_table = "auth_user"

    def get_permissions(self, defaults=None):
        defaults = defaults or default_permissions
        perms = {}
        for p in PERMISSIONS:
            v = self.is_superuser or p in defaults
            perms[p] = v
        return perms

    @property
    def all_permissions(self):
        return self.get_permissions()

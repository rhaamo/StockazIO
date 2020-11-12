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

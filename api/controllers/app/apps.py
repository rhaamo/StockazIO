from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "controllers.app"

    def ready(self):
        import controllers.users.signals  # noqa

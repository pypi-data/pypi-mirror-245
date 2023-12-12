from django.apps import AppConfig


class B2FormsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "b2_forms"

    def ready(self):
        import b2_forms.signals  # noqa: F401

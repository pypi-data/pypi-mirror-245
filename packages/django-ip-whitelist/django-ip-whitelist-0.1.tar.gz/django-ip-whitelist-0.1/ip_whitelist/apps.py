from django.apps import AppConfig


class SecurityConfig(AppConfig):
    name = "ip_whitelist"
    verbose_name = "IP whitelist"
    default_auto_field = "django.db.models.BigAutoField"

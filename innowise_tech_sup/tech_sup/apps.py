from django.apps import AppConfig


class TechSupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tech_sup'

    def ready(self):
        from . import signal

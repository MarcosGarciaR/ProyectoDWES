from django.apps import AppConfig


class CampingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'camping'

    def ready(self):
        import camping.signals

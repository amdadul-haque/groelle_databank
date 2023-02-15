from django.apps import AppConfig


class DatabankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'databank'

    def ready(self):
        import databank.signals

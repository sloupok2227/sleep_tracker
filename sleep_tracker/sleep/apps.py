from django.apps import AppConfig

class SleepConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sleep'

    def ready(self):
        import sleep.signals  # Убедитесь, что файл signals.py существует

class SleepConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sleep'

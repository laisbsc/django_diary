import os

from django.apps import AppConfig


class AiToolsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_tools'

    def ready(self):
        if os.environ.get('LOGFIRE_TOKEN'):
            import logfire
            logfire.instrument_django()

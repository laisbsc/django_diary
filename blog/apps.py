import os

from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        import logfire
        if os.environ.get('LOGFIRE_TOKEN'):
            logfire.instrument_django(capture_headers=True)
            logfire.instrument_system_metrics({
                'process.cpu.utilization': None,
                'system.cpu.simple_utilization': None,
                'system.memory.usage': ['available', 'used'],
                'system.memory.utilization': ['available', 'used'],
                'system.swap.utilization': ['used'],
                'system.network.io': ['transmit', 'receive'],
            })
            logfire.instrument_psycopg()
            logfire.instrument_pydantic_ai()

 # More details in logfire docs: https://pydantic.dev/docs/logfire/integrations/web-frameworks/django

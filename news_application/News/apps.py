from django.apps import AppConfig
from .functions.tweet import Tweet


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'News'

    def ready(self):
        import News.signals

    def tweet(self):
        Tweet()

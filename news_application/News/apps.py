from django.apps import AppConfig
from .functions.tweet import Tweet

Tweet.initialize(api_keys=
                 {
                     'consumer_key': Tweet.CONSUMER_KEY,
                     'consumer_secret': Tweet.CONSUMER_SECRET
                 })


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'News'

    def ready(self):
        import News.signals

    def tweet(self):
        Tweet()

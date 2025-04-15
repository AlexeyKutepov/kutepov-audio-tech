from django.contrib.syndication.views import Feed

from main.feed.custom_feed_generator import CustomFeedGenerator
from main.models import Post


class ArticleFeed(Feed):
    title = "Kutepov Audio Tech"
    link = "http://kutepov-audio-tech.ru"
    description = "Проектирование и изготовление аудио-оборудования"
    feed_type = CustomFeedGenerator

    def items(self):
        return Post.objects.order_by('-datetime')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

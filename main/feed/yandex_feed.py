from yaturbo import YandexTurboFeed

from main.models import Post


class YandexFeed(YandexTurboFeed):
    title = "Kutepov Audio Tech"
    link = "http://kutepov-audio-tech.ru"
    description = "Проектирование и изготовление аудио-оборудования"

    turbo_sanitize = True

    def items(self):
        return Post.objects.order_by('-datetime')

    def item_turbo(self, item):
        header = "<header><h1>{}</h1></header>".format(item.title)
        return header + item.content


from yaturbo import YandexTurboFeed

from main.models import Post


class YandexFeed(YandexTurboFeed):
    title = "Блог Алексея Кутепова"
    link = "http://kutepov-audio-tech.ru"
    description = "Разработка программного обеспечения и автоматизация бизнес-процессов"

    turbo_sanitize = True

    def items(self):
        return Post.objects.order_by('-datetime')

    def item_turbo(self, item):
        header = "<header><h1>{}</h1></header>".format(item.title)
        return header + item.content


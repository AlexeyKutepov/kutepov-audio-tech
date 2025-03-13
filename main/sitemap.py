from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from main.models import Post


class PostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.update_date


class StaticSitemap(Sitemap):
    priority = 0.6
    changefreq = 'never'
    i18n=True

    def items(self):
        return ['index', 'contacts', 'diy']

    def location(self, item):
        return reverse(item)

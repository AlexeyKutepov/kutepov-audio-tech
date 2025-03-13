"""akutepov URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView, RedirectView
from django.contrib.sitemaps.views import sitemap

from main.feed.article_feed import ArticleFeed
from main.feed.yandex_feed import YandexFeed
from main.sitemap import PostSitemap, StaticSitemap

sitemaps = {
    'posts': PostSitemap,
    'static': StaticSitemap,
}

urlpatterns = [
                  path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
                       name='django.contrib.sitemaps.views.sitemap'),
                  path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
                  path('ads.txt', TemplateView.as_view(template_name='ads.txt', content_type='text/plain')),
                  path('rss/', ArticleFeed(), name='rss'),
                  path('turbo/', YandexFeed(), name='turbo'),
                  path('i18n/', include('django.conf.urls.i18n')),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('', RedirectView.as_view(pattern_name='index', permanent=False))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
)

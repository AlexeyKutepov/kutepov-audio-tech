from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


class Feedback(models.Model):
    """
    Сообщения из формы обратной связи
    """
    email = models.EmailField()
    message = models.TextField()
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email


class Subscriber(models.Model):
    """
    Данные подписчиков
    """
    email = models.EmailField()
    datetime = models.DateTimeField(default=timezone.now)
    is_subscribed = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email


class Post(models.Model):
    """
    Пост
    """
    general_category = 'Информация'
    diy_category = 'DIY'
    category_classifier = (
        (general_category, 'Информация'),
        (diy_category, 'DIY'),
    )
    title = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    title_image = models.ImageField(upload_to="title_images")
    datetime = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    short_text = models.TextField()
    content = RichTextUploadingField('contents')
    is_published = models.BooleanField(default=False)
    category = models.CharField(max_length=15, choices=category_classifier)
    update_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/ru/blog/%s/" % self.url
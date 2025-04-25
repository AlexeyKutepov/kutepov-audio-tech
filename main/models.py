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
    title_image = models.ImageField(upload_to="posts/")
    datetime = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    short_text = models.TextField()
    content = RichTextUploadingField('content')
    is_published = models.BooleanField(default=False)
    category = models.CharField(max_length=100, choices=category_classifier)
    update_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/ru/blog/%s/" % self.url
    

class ProductInfo(models.Model):
    """
    Информация о продукции
    """
    guitar_effect_pedals_category = 'Педали эффектов'
    category_classifier = (
        (guitar_effect_pedals_category, 'Педали эффектов'),
    )
    name = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    image = models.ImageField(upload_to="products/")
    datetime = models.DateTimeField(default=timezone.now)
    short_text = models.TextField()
    description = RichTextUploadingField('description')
    is_published = models.BooleanField(default=False)
    category = models.CharField(max_length=100, choices=category_classifier)
    update_date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/ru/product/%s/" % self.url
    
    def get_discount(self):
        if self.old_price:
            return round((1 - (self.price / self.old_price)) * 100)
        return 0
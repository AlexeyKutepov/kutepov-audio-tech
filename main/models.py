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

    class Meta:
        ordering = ['id']
        verbose_name = 'сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.email


class Subscriber(models.Model):
    """
    Данные подписчиков
    """
    email = models.EmailField()
    datetime = models.DateTimeField(default=timezone.now)
    is_subscribed = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'подписчика'
        verbose_name_plural = 'Подписчики'

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

    class Meta:
        ordering = ['id']
        verbose_name = 'пост'
        verbose_name_plural = 'Посты'

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
    image = models.ImageField(
        upload_to="products/main/",
        verbose_name="Главное изображение"
    )
    datetime = models.DateTimeField(default=timezone.now)
    short_text = models.TextField()
    description = RichTextUploadingField('description')
    is_published = models.BooleanField(default=False)
    category = models.CharField(max_length=100, choices=category_classifier)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available = models.BooleanField(default=True)
    vk_url = models.URLField("VK ссылка", max_length=500, blank=True, default="")
    telegram_url = models.URLField("Telegram ссылка", max_length=500, blank=True, default="")

    class Meta:
        ordering = ['id']
        verbose_name = 'информацию о продукции'
        verbose_name_plural = 'Информация о продукции'

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
    
    # Метод для получения ВСЕХ изображений продукта
    def all_images(self):
        """Возвращает все изображения продукта (главное + дополнительные)"""
        images = [self.image]  # главное изображение
        images.extend([img.image for img in self.images.all()])  # дополнительные
        return images
    

class ProductImage(models.Model):
    """
    Изображения продукта
    """
    product = models.ForeignKey(
        ProductInfo, 
        on_delete=models.CASCADE,
        related_name='images'  # имя для обратной связи
    )
    image = models.ImageField(upload_to="products/")
    order = models.PositiveIntegerField(
        default=0,  # для сортировки изображений
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['order']  # автоматическая сортировка по порядку
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продуктов'

    def __str__(self):
        return f"Изображение для {self.product.name}"


class ContactLink(models.Model):
    """Ссылки для страницы контактов (социальные сети и т.п.)."""
    name = models.CharField('Название', max_length=100)
    url = models.URLField('Ссылка', max_length=500)
    icon_class = models.CharField('CSS класс иконки', max_length=100, blank=True, default='')  # например 'fab fa-telegram'
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Отображать', default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'ссылку для страницы контактов'
        verbose_name_plural = 'Ссылки для страницы контактов'

    def __str__(self):
        return self.name   
     
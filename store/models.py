from django.db import models
from django.urls import reverse
# from django.contrib.postgres.fields.jsonb import JSONField


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True)
    # specs = JSONField(default=dict, blank=True)  # {"Тип": "Фузз", "Питание": "9V"}

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])
    
    def get_discount_percent(self):
        if self.old_price:
            return int((1 - self.price / self.old_price) * 100)
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/')


class Cart(models.Model):
    session_key = models.CharField(max_length=40, blank=True, null=True)  # Для гостей
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)  # Для авторизованных
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price
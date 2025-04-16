from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Cart, CartItem, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение slug при вводе названия


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')
    list_filter = ('category', 'available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'available')  # Быстрое редактирование в списке


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview')
    
    def image_preview(self, obj):
        return format_html('<img src="{}" height="50"/>', obj.image.url)


class CartItemInline(admin.TabularInline):  # Товары в корзине внутри Cart
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'created_at')
    inlines = [CartItemInline]

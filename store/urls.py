from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Главная и категории
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    
    # Карточка товара (должен быть ПОСЛЕ категорий)
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Корзина
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
]
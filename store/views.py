from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def product_list(request, category_slug=None):
    products = Product.objects.filter(available=True)  # Только доступные товары
    
    # Фильтрация по категории (если slug передан)
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Пагинация (например, по 6 товаров на странице)
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    # Контекст для шаблона
    context = {
        'products': products,
        'category_slug': category_slug,  # Для выделения активной категории
    }
    
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    """
    Отображает детальную страницу товара.
    
    Args:
        request: HttpRequest-объект.
        slug (str): Уникальный идентификатор товара в URL.
    
    Returns:
        HttpResponse: Страница с подробной информацией о товаре.
    """
    # Получаем товар или 404
    product = get_object_or_404(
        Product,
        slug=slug,
        available=True  # Только доступные товары
    )
    
    # Похожие товары (из той же категории, исключая текущий)
    similar_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(
        id=product.id
    )[:4]  # Первые 4 товара
    
    # Контекст для шаблона
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    
    return render(request, 'store/product_detail.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Получаем или создаём корзину
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    # Добавляем товар в корзину
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart_detail')


def cart_detail(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first()
    
    context = {'cart': cart}
    return render(request, 'store/cart_detail.html', context)
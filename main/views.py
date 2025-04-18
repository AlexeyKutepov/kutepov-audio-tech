import logging

import sys
from django.core.mail import send_mail
from django.http import JsonResponse, Http404
from django.utils import timezone

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from kat import settings
from main.forms import FeedbackForm, SubscribeForm
from main.models import Feedback, Subscriber, Post
from store.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

logger = logging.getLogger(__name__)


def index(request):
    """
    Главная страница
    :param request:
    :return:
    """
    general_list = Post.objects.filter(is_published=True, category=Post.general_category).order_by('-datetime')
    general_len = len(general_list)


    products = Product.objects.filter(available=True)  # Только доступные товары
    
    # Пагинация (например, по 6 товаров на странице)
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    return render(
        request,
        "main/index.html",
        {
            'products': products,
            "general_list": general_list[:general_len],
        }
    )


def contacts(request):
    """
    Контакты
    :param request:
    :return:
    """
    is_send = None
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            if 'subject' in form.cleaned_data and form.cleaned_data['subject']:
                is_send = False
            elif 'email' not in form.cleaned_data and 'message' not in form.cleaned_data:
                is_send = False
            else:
                Feedback.objects.create(
                    email=form.cleaned_data['email'],
                    message=form.cleaned_data['message'],
                    datetime=timezone.now()
                )
                try:
                    send_mail(
                        "Новое сообщение",
                        'e-mail: ' + form.cleaned_data['email'] + '\n \nСообщение: ' + form.cleaned_data['message'],
                        getattr(settings, "EMAIL_HOST_USER", None),
                        [settings.EMAIL_ADDRESS, ],
                        fail_silently=False,
                    )
                except:
                    logger.error("Невозможно отправить e-mail сообщение: ", sys.exc_info()[0])
                is_send = True
    return render(
        request,
        "main/contacts.html",
        {"is_send": is_send}
    )


def subscribe(request):
    """
    Подписка
    :param request: request
    :return: json
    """
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subscriber_list = Subscriber.objects.filter(email=form.cleaned_data['email'])
            if len(subscriber_list) == 0:
                Subscriber.objects.create(
                    email=form.cleaned_data['email']
                )
            return JsonResponse({"result": "ok"})
        else:
            return JsonResponse({"result": "error"})


@csrf_exempt
def unsubscribe(request, id):
    """
    Отписка
    :param request:
    :return:
    """
    if request.method == 'POST':
        subscriber = Subscriber.objects.get(id=id)
        if subscriber:
            subscriber.is_subscribed = False
            subscriber.save()
            return JsonResponse({"result": "ok"})
        else:
            return JsonResponse({"result": "error"})


def blog(request):
    """
    Блог
    :param request:
    :return:
    """
    post_list = Post.objects.filter(is_published=True).order_by('-datetime')
    return render(
        request,
        "main/blog.html",
        {
            "post_list": post_list
        }
    )


def post(request, url):
    """
    Пост
    :param request:
    :param url:
    :return:
    """
    post_list = Post.objects.filter(url=url)
    if not post_list or len(post_list) == 0:
        raise Http404
    return render(
        request,
        "main/post.html",
        {
            "post": post_list[0]
        }
    )
